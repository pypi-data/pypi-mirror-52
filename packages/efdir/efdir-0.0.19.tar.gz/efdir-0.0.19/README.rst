======
ReadMe
======


Installation
------------
    ::
    
    $ pip3 install efdir


License
-------

- MIT



Quickstart
----------
- pip3 install efdir

- edit a cfg.rst file using bullet-list as below:

.. image:: /docs/images/rst.0.png

- run cmd **efdir cfg.rst wkdir** 
      
.. image:: /docs/images/mktree.0.png


Usage
-----

- using .rst 

    ::
 
         import efdir.mktree as emk
        
        
        # if the name end with a "$", it means this is a file, such as "xx$",  will touch a empty file named xx
        # else, it means this is a dir ,will make a dir
        
        rst_cfg = """
        - a
        
            - b   
        
                    - xx$
                    - yy
                    - zz
            - c
            - d
        - e
        - f
        """
        
        
        emk.mktree(rst_cfg,"./wkdir")
        #or directly from a cfg.rst file(filename must end with .rst)
        emk.fmktree("./cfg.rst","./wkdir")
        
        ######################
        TEST# tree wkdir
        wkdir
        ├── a
        │   ├── b
        │   │   ├── xx
        │   │   ├── yy
        │   │   └── zz
        │   ├── c
        │   └── d
        ├── e
        └── f
        
        8 directories, 1 file
        ######################
        
        
- using .json

    ::  
    
        import efdir.mktree as emk
        # if the name end with a "$", it means this is a file, such as "init.sh$",  will touch a empty file named init.sh
        # else, it means this is a dir ,will make a dir
        
        json_cfg = {
            "REPO":{
                "BACKUP" : {},
                "DRAFT" : {},
                "INIT" : {
                    "init.sh$":{}
                },
                "EDICT" : {
                    "IMGS":{
                        "img0.desc$":{},
                        "img1.desc$":{}
                    },
                    "DETAILS":{
                        "1.info$":{},
                        "2.info$":{}
                    },
                    "edict.py$":{}
                },
                "setup.py$":{},
                "README.md$":{},
                "LICENSE$":{},
                "install.sh$":{},
                "uninstall.sh$":{},
                "update.sh$":{},
                "pypiupload.sh$":{}
            }
        }
        
        emk.mktree(json_cfg,"./wkdir")
        #or directly from a cfg.json file(filename must end with .rst)
        emk.fmktree("./cfg.json","./wkdir") 
        

- from cmdline

    ::

        root@# efdir cfg.rst "rstwkdir"
        root@# tree rstwkdir
        root@# efdir cfg.json "jsonwkdir"
        root@# tree jsonwkdir

Features
--------

- mktree from .rst bullet-list config
- mktree from .json config


References
----------

* docutils
* shutil
