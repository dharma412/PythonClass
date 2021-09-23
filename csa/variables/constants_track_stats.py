# $Id: //prod/main/sarf_centos/variables/constants_track_stats.py#1 $
class track_stats:
    """
    Constants related to log file track_stats
    """
    LOCATION = '/data/pub/track_stats/prox_track.log'
    UNUSED = ' -E " ({VALUE}) unused"'
    SM_HIT_INACT = ' -E " ({VALUE}) sm-hit-inact"'
    LQ_HIT_INACT = ' -E " ({VALUE}) lg-hit-inact"'
    HQ_HIT_INACT = ' -E " ({VALUE}) hg-hit-inact"'
    SM_MIS_INACT = ' -E " ({VALUE}) sm-mis-inact"'
    SM_PRF_INACT = ' -E " ({VALUE}) sm-prf-inact"'
    LQ_PRF_INACT = ' -E " ({VALUE}) lg-prf-inact"'
    HQ_PRF_INACT = ' -E " ({VALUE}) hg-prf-inact"'
    LQ_PRF_INUSE = ' -E " ({VALUE}) lg-prf-inuse-latter"'
    HQ_PRF_INUSE = ' -E " ({VALUE}) hg-prf-inuse-latter"'
    LQ_HIT_INUSE = ' -E " ({VALUE}) lg-hit-inuse-latter"'
    HQ_HIT_INUSE = ' -E " ({VALUE}) hg-hit-inuse-latter"'
    SM_PRF_UNUSED = ' -E " ({VALUE}) sm-prf-unused"'
    LQ_PRF_UNUSED = ' -E " ({VALUE}) lg-prf-unused"'
    HQ_PRF_UNUSED = ' -E " ({VALUE}) hg-prf-unused"'
    SM_PRF_INUSE = ' -E " ({VALUE}) sm-prf-inuse"'
    LQ_PRF_INUSE_FIRST = ' -E " ({VALUE}) lg-prf-inuse-first"'
    HQ_PRF_INUSE_FIRST = ' -E " ({VALUE}) hg-prf-inuse-first"'
    SM_HIT_INUSE = ' -E " ({VALUE}) sm-hit-inuse"'
    LQ_HIT_INUSE_FIRST = ' -E " ({VALUE}) lg-hit-inuse-first"'
    HQ_HIT_INUSE_FIRST = ' -E " ({VALUE}) hg-hit-inuse-first"'
    SM_MIS_REUSE = ' -E " ({VALUE}) sm-mis-reuse"'
    SM_MIS_INUSE = ' -E " ({VALUE}) sm-mis-inuse"'
    LQ_MIS_INUSE = ' -E " ({VALUE}) lg-mis-inuse"'
    TRANSITORY = ' -E " ({VALUE}) transitory"'
    TUNNEL = ' -E " ({VALUE}) tunnel"'
    MISC = ' -E " ({VALUE}) misc"'

