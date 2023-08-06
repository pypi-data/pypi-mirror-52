======
ReadMe
======


Installation
------------
    ::
    
    $ pip3 install minidoc


License
-------

- MIT



Quickstart
----------
- *pip3 install minidoc*

- *make a workdir, such as "TEST"*
    
    ::
    
        mkdir TEST
        cd TEST
   
- *edit your code.tst.py  as below:*

    ::
        
        cat code.tst.py
        

.. image:: /docs/images/code.tst.py.00.png

- 

| *run cmd* **minidoc** ,
| *will auto exec the code in code.tst.py,* 
| *and auto save  the terminal screen-shot(or recording)* 
| *and auto generate a .rst doc-file* 
  
  ::
      
      minidoc
      tree
      TEST# tree
      .
      ├── code.tst.py
      ├── images------------------------------->generated svgs
      │   ├── __getitem__.svg
      │   └── __init__.svg
      └── Usage.rst---------------------------->generated .rst
      
      1 directory, 4 files
      TEST#

      
.. image:: /docs/images/code.tst.py.11.png
.. image:: /docs/images/code.tst.py.2.png



- *open generated .rst to check it*

.. image:: /docs/images/code.tst.py.3.png


- *minidoc -h*

    ::
        
        TEST# minidoc -h
        usage: minidoc [-h] [-tst TEST_FILE] [-codec CODEC] [-still STILL_FRAMES]
                       [-rows ROWNUMS] [-dst DST_DIR] [-title TITLE] [-tbot TITLE_BOT]
                       [-ebot ENTRY_BOT]
        
        optional arguments:
          -h,                   --help                       show this help message and exit
          -tst    TEST_FILE,    --test_file TEST_FILE        .tst.py file name,default = "code.tst.py"
          -codec  CODEC,        --codec CODEC                .tst.py file codec,default = "utf-8"
          -still  STILL_FRAMES, --still_frames STILL_FRAMES  generate screen shot,default = True (which means still image but not recording)
          -rows   ROWNUMS,      --rownums ROWNUMS            screen height,default = 30
          -dst    DST_DIR,      --dst_dir DST_DIR            destination svg dir, default ="./images"
          -title  TITLE,        --title TITLE                parent title, default = "Usage"
          -tbot   TITLE_BOT,    --title_bot TITLE_BOT        parent title bottom char, default = '='
          -ebot   ENTRY_BOT,    --entry_bot ENTRY_BOT        entry title bottom char, default = '-'


Usage
-----

- from code

    ::
        
        In progressing.....
            

- from cmdline

    ::
       
        # screen shot
        root@# minidoc -tst code.rst.py -dst ./images
        
        # screen recording
        root@# minidoc -tst code.rst.py -dst ./images -still false 
        
        # on current dir,screen shot
        root@# minidoc -still true
        
        # on current dir,screen recording
        root@# minidoc -still false


- from docstring only one level(experimental,no recursive support, since only one level AST walked)
    
    ::
        
        root@# minidoc_from_docstring -proj dtable




Features
--------

- auto generate .rst doc from .tst.py
- auto exec test-code in .tst.py 
- auto record the screen and save as .svg


Restrict
--------

- currently only support python3

TODO
----

- javascript
- lua
- tclsh


References
----------

* termtosvg
* elist
* efdir
* estring
