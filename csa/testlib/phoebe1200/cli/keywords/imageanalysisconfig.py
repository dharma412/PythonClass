#!/usr/bin/env python -tt
# $Id: //prod/main/sarf_centos/testlib/phoebe1200/cli/keywords/imageanalysisconfig.py#1 $ $DateTime: 2019/03/22 01:36:06 $ $Author: aminath $

from common.cli.clicommon import CliKeywordBase


class imageanalysisconfig(CliKeywordBase):
    """Configure the IronPort Image Analysis settings.

    cli -> imageanalysisconfig

    Valid IIA feature key must be installed before using this
    CLI command
    """

    def get_keyword_names(self):
        return ['image_analysis_config_setup']

    def image_analysis_config_setup(self, *args):
        """Configure the IronPort Image Analysis settings.

        imageanalysisconfig -> setup

        *Parameters:*
        - `use_iia`: you like to use IronPort Image Analysis, yes or no
        - `license_agreement`: whether you want to accept license agreement,
        yes or no
        - `img_sensitivity`: the image analysis sensitivity. Either
        a value between 0 (least sensitive) and 100 (most sensitive). As
        sensitivity increases, so does the false positive rate. The default
        setting of 65 is recommended
        - `img_clean_verd`: the range for a CLEAN verdict. Either
        the upper bound of the CLEAN range - a value between 0 and 98.
        The default setting of 49 is recommended
        - `img_suspect_verd`: the range for a SUSPECT verdict. Enter the upper
        bound of the SUSPECT range by entering a value between 50 and 99. The
        default setting of 74 is recommended
        - `clean_score`: score you wish to consider for a clean message,
        number from 0 to 100
        - `suspect_score`: score you wish to consider for a suspect message,
        number from 0 to 100
        - `confirm_disable`: whether you want to disable the IronPort Image Analysis
        feature (only if use_iia is set to NO), either yes or no
        - `skip_smaller`: whether you like to skip scanning of images smaller than
        a specific size, either yes or no
        - `min_size`: minimum image size to scan in pixels, representing either
        height or width of a given image

        *Exceptions:*
        - `FeaturekeyError`: if no valid IIA feature key installed

        *Return:*
        Raw output

        *Examples:*
        | Image Analysis Config Setup | use_iia=Yes | img_sensitivity=63 |
        | ... | img_clean_verd=40 | img_suspect_verd=70 | clean_score=10 |
        | ... | suspect_score=50 | skip_smaller=No | min_size=50 |
        """
        kwargs = self._convert_to_dict(args)
        self._cli.imageanalysisconfig().setup(**kwargs)
