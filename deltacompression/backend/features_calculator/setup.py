from distutils import core # pylint: skip-file

FEATURES = core.Extension("features_calculator",
                          sources=["features_calculator.c"])

core.setup(name="features_calculator",
           version="1.0",
           description="Calculating features for the given chunk",
           ext_modules=[FEATURES])
