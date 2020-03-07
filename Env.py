from asyncore import file_dispatcher

import pandas as pd

import plotly.offline as py #visualization

import plotly.graph_objs as go#visualization


# add desired grid

class Env:
    def __init__(self, filename):
        with open(filename, "r") as f:
            # I'm assuming the file could be sparse

            lines = [l for l in f.read().splitlines() if l != ""]
            index = lines.index("scrambled_image")


            assert lines[0] == "unscrambled_image"
            assert lines[1][0:5] == "size="
            size = int(lines[1][5:])
            desiredState = [[[0 for _ in range(size)] for _ in range(size)] for _ in range(size)]
            for l in lines[2:index]:
                # add to state
                eIndex = l.index("=")
                pos = l[:eIndex]
                posStr = pos.split(",")
                x = int(posStr[0])
                y = int(posStr[1])
                z = int(posStr[2])

                color = l[eIndex+1:].strip("\"")

                desiredState[x][y][z] = color

            assert lines[index] == "scrambled_image"
            assert lines[index+1][0:5] == "size="
            dSize = int(lines[index+1][5:])
            assert dSize == size
            state = [[[0 for _ in range(size)] for _ in range(size)] for _ in range(size)]
            for l in lines[index+2:]:
                # add to state
                eIndex = l.index("=")
                pos = l[:eIndex]
                posStr = pos.split(",")
                x = int(posStr[0])
                y = int(posStr[1])
                z = int(posStr[2])

                color = l[eIndex + 1:].strip("\"")

                state[x][y][z] = color

            self.state = state
            self.dState = desiredState
            self.state_dataFrame = self.convert_to_dataframe(state)
            self.dState_dataFrame = self.convert_to_dataframe(desiredState)
            self.s = size

    def stateEquals(self, mem):
        return self.state == mem

    def done(self):
        return self.state == self.dState

    def blockAt(self, x, y):
        for z in reversed(range(self.s)):
            if self.state[x][y][z] != "":
                return self.state[x][y][z], z
        return None
    
    def desiredBlockAt(self, x, y):
        for z in reversed(range(self.s)):
            if self.state[x][y][z] != "":
                return self.dState[x][y][z], z
        return None

    def getSize(self):
        return self.s

    def addBlock(self, x, y, tuple):
        # wip
        color = tuple[0]
        z = tuple[1]


    def takeBlock(self, x, y):
        # return none if we can't take...
        #wip
        for z in reversed(range(self.s)):
            if self.state[x][y][z] != "":
                color = self.state[x][y][z]
                self.state[x][y][z] = ""
                return color, z
        return "", 0
    
    def convert_to_dataframe(self, State):
        df = pd.DataFrame(columns=['X', 'Y', 'Z', 'RGB'])
        
        for x in range(len(State)):
            for y in range(len(State[x])):
                for z in range(len(State[x][y])):
                    if State[x][y][z] == '':
                        df = df.append({'X': x, 'Y': y, 'Z': z, 'RGB': ''}, ignore_index=True)
                    else:
                        RGB_values = State[x][y][z].split('_')
                        df = df.append({'X': x, 'Y': y, 'Z': z, 'RGB': 'rgb({0},{1},{2})'.format(RGB_values[0],RGB_values[1],RGB_values[2])}, ignore_index=True)
    
        return df

    def plot_state(self, State):
        # separate empty and non empty squares
        empty_blocks    = State[State['RGB'] == '']
        full_blocks     = State[State['RGB'] != '']


        trace1 = go.Scatter3d(x = empty_blocks["X"],
                      y = empty_blocks["Y"],
                      z = empty_blocks["Z"],
                      mode = "markers",
                      opacity=0.5,
                      name = "Empty Space",
                      marker = dict(size = 10,color = "grey")
                     )        
        trace2 = go.Scatter3d(x = full_blocks["X"],
                      y = full_blocks["Y"],
                      z = full_blocks["Z"],
                      mode = "markers",
                      name = "Filled Space",
                      marker = dict(size = 10,color = "green")
                     )
        layout = go.Layout(dict(title = "State of the Structure",
                        scene = dict(camera = dict(up=dict(x= 0 , y=0, z=0),
                                                   center=dict(x=0, y=0, z=0),
                                                   eye=dict(x=1.25, y=1.25, z=1.25)),
                                     xaxis  = dict(title = "X value",
                                                   gridcolor='rgb(255, 255, 255)',
                                                   zerolinecolor='rgb(255, 255, 255)',
                                                   showbackground=True,
                                                   backgroundcolor='rgb(230, 230,230)'),
                                     yaxis  = dict(title = "Y value",
                                                   gridcolor='rgb(255, 255, 255)',
                                                   zerolinecolor='rgb(255, 255, 255)',
                                                   showbackground=True,
                                                   backgroundcolor='rgb(230, 230,230)'
                                                  ),
                                     zaxis  = dict(title = "Z value",
                                                   gridcolor='rgb(255, 255, 255)',
                                                   zerolinecolor='rgb(255, 255, 255)',
                                                   showbackground=True,
                                                   backgroundcolor='rgb(230, 230,230)'
                                                  )
                                    ),
                        height = 700,
                       )
                  )
                  

        data = [trace1,trace2]
        fig  = go.Figure(data = data,layout = layout)
        py.plot(fig)
