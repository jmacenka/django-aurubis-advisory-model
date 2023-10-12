

import io
import base64
import pandas as pd
import matplotlib.pyplot as plt

# Just load dummy data form file and return a pandas plot
SRC_FILE = './../dev/data/Celox ppm O2 [ppm].csv'

df = pd.read_csv(SRC_FILE, sep=';', index_col=0)

buffer = io.BytesIO()
df.plot()
plt.savefig(buffer, format='png')
buffer.seek(0)
image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
buffer.close()
