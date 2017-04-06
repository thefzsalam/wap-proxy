from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pathlib import Path
from subprocess import run

# TODO: Move config vars up the level

# Config Vars
FULLIMG_SIZE        = (256,256)
CROPIMG_RESIZE_PCT  = '50%'
CROPIMG_SIZE        = (128,1024)
CROPIMG_PREGAMMA    = 1.2
CROPIMG_POSTGAMMA   = 0.4
IMGFULL             = "imgfull.jpg"
IMGPART_SHELL_PAT   = "imgpart_%d.jpg"
IMGPART_PY_PAT      = "imgpart_{}.jpg"
IMGPART_STARTSWITH  = "imgpart_"


class Imagify:
    """
        Variables:
            root_path       : Root cache dir of imagify module
            last_url_file   : The file where the url of currently 
                              imagified page is stored
        Directory Structure:
            - root/                  (Provided by top level application code)
            --- last_url_file        (file to store the url of cached site)
    """

    def __init__(self, root_path):
        self.root_path     = root_path
        self.last_url_file = root_path/'last_url.txt'

    def _imagify(self, url_str, imgfile_str, width, height):
        """ Download the given webpage and save it.
            Return the title of the webpage as seen by the browser.
        """
        capabilities = DesiredCapabilities.PHANTOMJS
        capabilities["phantomjs.page.settings.userAgent"] =\
                "Opera/9.80 (J2ME/MIDP; Opera Mini/4.4.2864/27.1382; U; en) "+\
                "Presto/2.8.119 Version/11.10"
        driver = webdriver.PhantomJS(desired_capabilities=capabilities)
        driver.set_window_size(width,height)
        driver.get(url_str)
        driver.save_screenshot(self.root_path/imgfile_str)
        title = driver.title
        driver.close()
        return title

    def _breakup_images(self,imgfile_str,
                       croppedimg_patstr,
                       crop_w, crop_h,
                       resize_pct, pregamma_frac, postgamma_frac):
        """ Crop the given image and break it into pieces of given size
        """
        run(['convert',imgfile_str,
                '-gamma', str(pregamma_frac),
                '-resize', str(resize_pct),
                '-gamma', str(postgamma_frac),
                '-crop', str(crop_w)+'x'+str(crop_h),
                croppedimg_patstr
            ],
            cwd = self.root_path)
    
    def get_lasturl(self):
        """ Returns last_url """
        if not self.last_url_file.is_file():
            return ""
        f = open(self.last_url_file)
        last_url = f.readline().strip()
        f.close()
        return last_url
    
    def _save_lasturl(self,url_str):
        f = open(self.last_url_file,'w')
        f.write(url_str)
        f.write('\n')
        f.close()
    
    def _cleanup_imgcache(self):
        # unlink means remove
        for p in self.root_path.iterdir():
            if p.is_file():
                p.unlink()

    def get_no_of_tiles(self):
        return len(
                [p.name for p in self.root_path.iterdir() \
                if p.name.startswith(IMGPART_STARTSWITH)]
            )
                

    def imagify(self, url_str):
        """ Imagifies given url, overwriting the cache
        """
        self._cleanup_imgcache()
        title = self._imagify(url_str,IMGFULL,*FULLIMG_SIZE)
        self._breakup_images(IMGFULL,IMGPART_SHELL_PAT,
                             *CROPIMG_SIZE, CROPIMG_RESIZE_PCT,
                             CROPIMG_PREGAMMA, CROPIMG_POSTGAMMA)
        self._save_lasturl(url_str)
        return title

    def get_tile(self,index):
        max_index = self.get_no_of_tiles() - 1
        if index>max_index:
            raise InvalidIndex(index,max_index)
        return self.root_path/IMGPART_PY_PAT.format(index)
    


class ImagifyException(Exception):
    """ Base class for exception in this module """

class InvalidIndex(ImagifyException):
    def __init__(self,index,max_index):
        self.index = index
        self.max_index = max_index
        self.message = "You tried to access imagify tile with index {}, "+\
                       "which is unavailable. Max available index is {}"\
                       .format(index,max_index)
