from distutils.core import setup

setup(
    name = "CRUDAPP",
    
    version="0.1.0",
    
    packages=["crudapp"],

    #include_package_data = True,

    requires=[
               "flask",
               "pandas",
               "datatime",
               "PyJWT",
               "re",
    ],
)
