# %%
import CleanData as cd
import DataExplore as de
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('report_template.html')