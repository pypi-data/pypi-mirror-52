from .filterrecording import FilterRecording
import numpy as np

try:
    from scipy import special
    from scipy.signal import iirnotch, filtfilt
    HAVE_NFR = True
except ImportError:
    HAVE_NFR = False

class NotchFilterRecording(FilterRecording):

    preprocessor_name = 'NotchFilter'
    installed = HAVE_NFR  # check at class level if installed or not
    preprocessor_gui_params = [
        {'name': 'freq', 'type': 'float', 'value':3000.0, 'default':3000.0, 'title': "Frequency"},
        {'name': 'q', 'type': 'int', 'value':30, 'default':30, 'title': "Quality factor"},
        {'name': 'chunk_size', 'type': 'int', 'value': 30000, 'default': 30000, 'title':
            "Chunk size for the filter."},
        {'name': 'cache', 'type': 'bool', 'value': False, 'default': False, 'title':
            "If True filtered traces are computed and cached"},
    ]
    installation_mesg = "To use the NotchFilterRecording, install scipy: \n\n pip install scipy\n\n"  # error message when not installed

    def __init__(self, recording, freq=3000, q=30, chunk_size=30000, cache=False):
        assert HAVE_NFR, "To use the NotchFilterRecording, install scipy: \n\n pip install scipy\n\n"
        self._freq = freq
        self._q = q
        FilterRecording.__init__(self, recording=recording, chunk_size=chunk_size, cache=cache)
        self.copy_channel_properties(recording)
        if cache:
            self._traces = self.get_traces()

    def filter_chunk(self, *, start_frame, end_frame):
        padding = 3000
        i1 = start_frame - padding
        i2 = end_frame + padding
        padded_chunk = self._read_chunk(i1, i2)
        filtered_padded_chunk = self._do_filter(padded_chunk)
        return filtered_padded_chunk[:, start_frame - i1:end_frame - i1]

    def _create_filter_kernel(self, N, sampling_frequency, freq_min, freq_max, freq_wid=1000):
        # Matches ahb's code /matlab/processors/ms_bandpass_filter.m
        # improved ahb, changing tanh to erf, correct -3dB pts  6/14/16
        T = N / sampling_frequency  # total time
        df = 1 / T  # frequency grid
        relwid = 3.0  # relative bottom-end roll-off width param, kills low freqs by factor 1e-5.

        k_inds = np.arange(0, N)
        k_inds = np.where(k_inds <= (N + 1) / 2, k_inds, k_inds - N)

        fgrid = df * k_inds
        absf = np.abs(fgrid)

        val = np.ones(fgrid.shape)
        if freq_min != 0:
            val = val * (1 + special.erf(relwid * (absf - freq_min) / freq_min)) / 2
            val = np.where(np.abs(k_inds) < 0.1, 0, val)  # kill DC part exactly
        if freq_max != 0:
            val = val * (1 - special.erf((absf - freq_max) / freq_wid)) / 2;
        val = np.sqrt(val)  # note sqrt of filter func to apply to spectral intensity not ampl
        return val

    def _do_filter(self, chunk):
        sampling_frequency = self._recording.get_sampling_frequency()
        M = chunk.shape[0]
        chunk2 = chunk
        fn = 0.5 * float(self.get_sampling_frequency())
        # Do the actual filtering with a DFT with real input
        b, a = iirnotch(self._freq / fn, self._q)

        if np.all(np.abs(np.roots(a)) < 1) and np.all(np.abs(np.roots(a)) < 1):
            chunk_filtered = filtfilt(b, a, chunk2, axis=1)
        else:
            raise ValueError('Filter is not stable')
        return chunk_filtered

    def _read_chunk(self, i1, i2):
        M = len(self._recording.get_channel_ids())
        N = self._recording.get_num_frames()
        if i1 < 0:
            i1b = 0
        else:
            i1b = i1
        if i2 > N:
            i2b = N
        else:
            i2b = i2
        ret = np.zeros((M, i2 - i1))
        ret[:, i1b - i1:i2b - i1] = self._recording.get_traces(start_frame=i1b, end_frame=i2b)
        return ret


def notch_filter(recording, freq=3000, q=30, chunk_size=30000, cache=False):
    '''
    Performs a notch filter on the recording extractor traces using scipy iirnotch function.

    Parameters
    ----------
    recording: RecordingExtractor
        The recording extractor to be notch-filtered.
    freq: int or float
        The target frequency of the notch filter.
    q: int
        The quality factor of the notch filter.
    chunk_size: int
        The chunk size to be used for the filtering.
    cache: bool
        If True, filtered traces are computed and cached all at once (default False).

    Returns
    -------
    filter_recording: NotchFilterRecording
        The notch-filtered recording extractor object

    '''
    return NotchFilterRecording(
        recording=recording,
        freq=freq,
        q=q,
        chunk_size=chunk_size,
        cache=cache,
    )
