
import setuptools

with open("./README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dj-querytools",
    version="0.2.0",
    author="AppointmentGuru",
    author_email="tech@appointmentguru.co",
    description="Some utility functions to perform complex queries with the Django ORM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/SchoolOrchestration/libs/dj-querytools",
    packages=['querytools'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)