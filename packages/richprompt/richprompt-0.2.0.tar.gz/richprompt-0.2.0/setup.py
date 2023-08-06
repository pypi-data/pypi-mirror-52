from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name="richprompt",
        version="0.2.0",
        url="https://github.com/lewisacidic/richprompt",
        author="Rich Lewis",
        author_email="opensource@richlew.is",
        description="A better IPython prompt",
        long_description=open("README.md").read(),
        long_description_content_type="text/markdown",
        license="MIT",
        keywords=["ipython", "prompt"],
        packages=find_packages(),
        install_requires=["ipython"],
        entry_points={
            "ipython_startup_hook": "richprompt = richprompt.startup:load"
        },
        extras_require={
            "hook": ["ipython-startup-hook"]
        }
    )
