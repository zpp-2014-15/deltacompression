from distutils import core

features = core.Extension("features",
                          sources=["features.c"])

core.setup(name="features",
           version="1.0",
           description="Calculating features for the given chunk",
           ext_modules=[features])
