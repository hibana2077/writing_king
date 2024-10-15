# import plotly.graph_objects as go
# # data = {'January': [10, 20, 60], 'February': [30, 40, 70], 'March': [50, 60, 80], 'April': [70, 80, 90], 'May': [90, 100, 110], 'June': [110, 120, 130], 'July': [130, 140, 150], 'August': [150, 160, 170], 'September': [170, 180, 190], 'October': [190, 200, 210], 'November': [210, 220, 230], 'December': [230, 240, 250]}

# x = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
# y = [
#     [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120],
#     [30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140],
#     [60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170]
# ]

# fig = go.Figure()
# for i in range(len(y)):
#     fig.add_trace(go.Scatter(x=x, y=y[i], mode='lines', name='lines'))

# fig.update_layout(title="Practice History", xaxis_title="Practice Times", yaxis_title="Scores")

# fig.show()

x = [1,2,3,4,5,6,7,8,9,10]

print(x[-11:])