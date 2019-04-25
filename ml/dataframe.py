import pandas as pd
import folium

class merge_dataset():
    def __init__(self,hl):
        self.hl = hl

    def merge(self,  columns_to_join):

        for i in range(len(self.hl)):
            self.hl[i] = self.hl[i][['DEPTH', 'lat', 'long'] + columns_to_join].dropna()

        df = pd.concat([self.hl[i] for i in range(len(self.hl))])
        df = df.reset_index(drop=True)
        # column_to_normalize = ['DEPTH'] + columns_to_join
        # for column in column_to_normalize:
        #     df[column] = (df[column] - df[column].min()) / (df[column].max() - df[column].min())
        return df


class populate():
    def __init__(self,grid_poly):
        self.grid_poly = grid_poly
        self.well_number_in_m = 1

    def populated_dataframe(self,hl):
        main = pd.DataFrame(columns=['DEPTH', 'lat', 'long'])
        for i in range(len(self.grid_poly)):
            dummy = pd.DataFrame(hl[0]['DEPTH'].reset_index(drop=True), columns=['DEPTH'])
            dummy['lat'] = self.grid_poly[i].x
            dummy['long'] = self.grid_poly[i].y
            main = pd.concat([main, dummy])
        main.reset_index(drop=True, inplace=True)
        return main


    def map_(self):
        if (self.well_number_in_m == 1):
            self.m = folium.Map(
                location=[self.grid_poly[0].x, self.grid_poly[0].y],
                zoom_start=12,
                tiles='Stamen Terrain'
            )
            folium.LayerControl().add_to(self.m)

        for i in range(len(self.grid_poly)):

            folium.Marker([self.grid_poly[i].x, self.grid_poly[i].y],
                          popup='<i>Well </i>' + str(self.well_number_in_m) + '   ( ' + str(self.grid_poly[i].x) + ','
                                + str(self.grid_poly[0].y) + ' )').add_to(self.m)
            self.well_number_in_m = self.well_number_in_m + 1
        return self.m



