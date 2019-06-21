import helper
import pytest
import logger
import utils

class TestMaHelper:
    def setup_class(self):
        self.helper = helper.MaHelper()
        
    def test_ma5(self):
        assert self.helper
        ai=[12.21, 12.49, 12.57, 12.73, 12.35, 12.23, 12.16]
        ma5_label=['-','-','-','-',12.47, 12.474, 12.408]
        ma5 = self.helper.getMa(5, ai) 
        logger.info(None, "array input: %s", ai)
        logger.info(None, "lable: %s", ma5_label)
        logger.info(None, "ma5: %s", ma5)
        assert utils.compare_array(ma5_label, ma5)
        
