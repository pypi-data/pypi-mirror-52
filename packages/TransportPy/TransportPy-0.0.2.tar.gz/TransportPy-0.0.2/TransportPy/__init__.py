name="transplan"
def plot_matrix(ufm="",df=None,Title='',shp="",zone_name_in_shp='zone',OD='O',variable_name='Variable',group_by='sum',bins=9,location=[51.704740, -0.042465],zoom_start=9,tiles = "Stamen Toner",epsg=3857,XEXES="C:\\SATWIN\\XEXES_11.3.12W_MC"):
        """
        plot_matrices takes the following inputs:
                ufm: SATURN ufm matrix
                shp: shapefile with the zoning system
                variable_name: the name of the variable we want to plot
                location: the starting point where the plot will be centred
                zoom_start: initial zoom
                tiles: background styling
                epsg: Projection system of the shp
                XEXES: Location of your SATURN XEXES of preference

        plot_matrices returns an html with a choropleth of the input matrix values in the input areas of the .shp"""
        def read_ufm(file, MX="C:\\SATWIN\\XEXES_11.3.12W_MC\\$MX.exe", remove_txt=True, clean_up=True):
                from os import system, remove
                from pandas import read_csv
                import time
                keysfile = 'temp.key'
                text = '          13                                                                2000\n          16                                                                2604\n           9                                                                2604\n\n           0                                                                2604\n           0                                                                2000\ny                                                                           9200'
                f = open(keyfile,"w+")
                f.write(text)
                f.close()
                time.sleep(2)
                command = MX + " '" + file + "' " + "KEY temp.key VDU vdu"
                system(command)
                results_txt = file[:-3]+"TXT"
                time.sleep(1)
                matriz = read_csv(results_txt,index_col=None, delim_whitespace=True, header=None, names=['Origin', 'Destination', 'UserClass', variable_name])
                list(map(lambda x : remove(x), [results_txt, 'vdu.VDU',results_txt[:-3]+"LPX",'temp.key']))
                return(matriz)
        import matplotlib.pyplot as plt
        import geopandas as gpd
        import folium
        import pandas as pd
        import numpy as np
        crs='EPSG'+str(epsg)
        zones=gpd.read_file(shp)
        MX=XEXES+"\\$MX.exe"
        if ufm !='':
            ufm=ufm.replace("/","\\\\")
            ufm=ufm.replace(".ufm","")
            ufm=ufm.replace(".UFM","")
            ufmn=ufm.split('\\')[-1][-4]
            df=read_ufm(ufm,MX=MX)
        else:
            ufmn='Matrix'
        df=df[df['Origin']!=df['Destination']]
        if OD == 'O':
                df_org=df.groupby(['Origin']).agg({variable_name:group_by}).reset_index()
                name='Origins'
                legend_name='Origin ' + variable_name
                df_zones=pd.merge(zones,df_org,left_on=zone_name_in_shp,right_on='Origin')
        if OD == 'D':
                df_org=df.groupby(['Destination']).agg({variable_name:group_by}).reset_index()
                name='Destinations'
                legend_name='Destination ' + variable_name
                df_zones=pd.merge(zones,df_org,left_on=zone_name_in_shp,right_on='Destination')
        df_zones.geometry=df_zones.geometry.to_crs(epsg=epsg)
        df_zones['id']=df_zones.index.astype(str)
        somewhere=folium.Map(crs=crs,location=location,zoom_start=zoom_start,tiles = tiles)
        folium.Choropleth(
        geo_data=df_zones.geometry,
        name=name,
        data=df_zones[['id',variable_name]],
        columns=['id',variable_name],
        key_on='feature.id',
        fill_color='YlOrRd',
        fill_opacity=0.8,
        line_opacity=0.2,
        legend_name=legend_name,
        smooth_factor=1,
        bins=bins,
        reset=True).add_to(somewhere)
        def style_function(feature):
                return {'fillOpacity': 0,
                'weight': 0,
                'fillColor': '#black'}
        def g(geom,zones,Var,epsg):
                a=gpd.GeoSeries(geom).simplify(0.5)
                epsg='epsg:'+str(epsg)
                a.crs={'init':epsg}
                folium.GeoJson(a,control=False,overlay=False,name='zones',tooltip=folium.Tooltip('Zone: ' + str(zones) + ' ; '+variable_name +  ' ' + str(round(Var,2))),style_function =style_function).add_to(somewhere)
        if OD == 'O':
                np.vectorize(g)(df_zones.geometry,df_zones.Origin,df_zones[variable_name],epsg)
        else:
                np.vectorize(g)(df_zones.geometry,df_zones.Destination,df_zones[variable_name],epsg)
        if Title !='':
                somewhere.save(Title + legend_name +'.html')
        else:
                somewhere.save(ufmn + legend_name +'.html')

def read_ufm(file, MX="C:\\SATWIN\\XEXES_11.3.12W_MC\\$MX.exe", remove_txt=True, clean_up=True):
        """
        read_ufm takes the following inputs:
                file: the UFM matrix you wish to read
                MX: location of you $MX.exe verison of preference
        """
        from os import system, remove
        from pandas import read_csv
        import time
        keyfile = 'temp.key'
        text = '          13                                                                2000\n          16                                                                2604\n           9                                                                2604\n\n           0                                                                2604\n           0                                                                2000\ny                                                                           9200'
        f = open(keyfile,"w+")
        f.write(text)
        f.close()
        time.sleep(2)
        command = MX + " '" + file + "' " + "KEY temp.key VDU vdu"
        system(command)
        results_txt = file[:-3]+"TXT"
        time.sleep(1)
        matriz = read_csv(results_txt,index_col=None, delim_whitespace=True, header=None, names=['Origin', 'Destination', 'UserClass', 'Variable'])
        list(map(lambda x : remove(x), [results_txt, 'vdu.VDU',results_txt[:-3]+"LPX",'temp.key']))
        return(matriz)
def satall(DAT = "", UFM = "", PASSQ = None, PATH = "C:/SATWIN/XEXES_11.3.12W_MC"):
    """
    satall takes the following inputs:
        DAT: ".dat" main network file relative or absolute path
        UFM: ".ufm" matrix of trips
        PASSQ: PASSQ ".dat"
        PATH: the path to your SATURN XEXES of choice

    satall assigns the ufm matrix to the network defined in the dat file
    """
    from os import system, remove
    DAT=DAT.replace("/", "\\\\")
    DAT=DAT.replace(".dat", "")
    DAT=DAT.replace(".Dat", "")
    UFM=UFM.replace("/","\\\\")
    UFM=UFM.replace(".ufm","")
    UFM=UFM.replace(".UFM","") 
    if PASSQ is None:
        text = "SET PATH="+PATH+" CALL SATURN "+DAT+" "+UFM
        f = open("saturn_assing.bat","w+")
        f.write(text)
        f.close()
    else:
        PASSQ=PASSQ.replace("/", "\\\\")
        PASSQ=PASSQ.replace(".dat", "")
        PASSQ=PASSQ.replace(".Dat", "")
        text = "SET PATH="+PATH+"\nCALL SATURN "+PASSQ+" "+UFM+"\nCALL SATURN "+UFM+" PASSQ "+PASSQ
        f = open("saturn_assing.bat","w+")
        f.write(text)
        f.close()
    system("saturn_assing.bat")
def write_ufm(file,matrix=None, MX="C:\\SATWIN\\XEXES_11.3.12W_MC\\$MX.exe", remove_txt=True, clean_up=True):
    """
    write_ufm takes the following inputs:
        file: the name of the ".csv"
        matrix: the matrix to be written in ufm format
    """
    from os import system, remove
    import pandas as pd
    txtName = file[:-4]+".csv"
    pd.set_option('display.float_format', lambda x: '%.10f' % x)
    if file != None:
        matrix.to_csv(txtName,index=False)
    keyfile = 'temp.key'
    text = "           1                                                                2004\n" + txtName+"\n           2                                                                2030\n           8                                                                2031\n           1                                                                2030\n          13                                                                2000\n           0                                                                2604\n          14                                                                2000\n           1                                                                2600\n"+ file +"\nTITLE UNSET                                                                 9260\n           0                                                                2640\n           0                                                                2000\ny                                                                           9200"
    f = open(keyfile,"w+")
    f.write(text)
    f.close()
    command = MX + " I KEY temp.key VDU vdu"
    system(command)
    list(map(lambda x : remove(x), ['vdu.VDU','temp.key',txtName]))
def read_emmedotmat(file,save=True,savepath='Data path'):
    '''
    Read_emme takes the following inputs:
        file: emme matrix you wish to read
        save: True if you'd wish to save your matrix on pickle format
        savepath= path where you want the pickle to be saved set to your working folder by default
    returns the matrix or list of matrices contained in an .mat file
    '''
    from os import path
    import re
    from pandas import read_csv,to_pickle,to_numeric
    if savepath == 'Data path':
        savepath = path.abspath(path.dirname(file))
    matrix_file = open(file,'r')
    matrix=matrix_file.readlines()
    a=0
    for line in matrix:
        if line[0] in ['c','t','d']:
            a += 1
        else: 
            break
    matrix_file.close()
    matrix= read_csv(file,index_col=None, sep='~', header=None, skiprows=a ,names=['Column1'])
    matrix=matrix[matrix.Column1.str[0]!='d']
    matrix=matrix.reset_index(drop=True)
    indexes= matrix.index[matrix.Column1.str[0]=='a']
    if len(indexes)==1:
        b=1
        a=len(matrix)
        matrices=matrix.iloc[b:a]
        matrices = matrices['Column1'].str.split(r'\D', n = 2, expand = True)
        matrices2 = matrices[2].str.split(":", n = 2, expand = True)
        matrices[0]=matrices[1]
        matrices[1]=matrices2[0]
        matrices[2]=matrices2[1]
        matrices.columns = ['Origin','Destination','km']
        matrices[['Origin', 'Destination', 'km']]=matrices[['Origin', 'Destination', 'km']].apply(to_numeric)
        matrices[['Origin','Destination']]=matrices[['Origin','Destination']].astype(int)
        if save == True:
            matrix_title=str(matrix.iloc[indexes[1:2]].values[0])[15:-2]
            matrix_title=matrix_title.replace(", ", " ")
            matrix_title=matrix_title.split()
            for chunks in range(len(matrix_title)):
                if chunks == 0 or chunks == 1:
                    continue
                if chunks == 2:
                    new_matrix_title=matrix_title[chunks]
                else:    
                    new_matrix_title=new_matrix_title+'_'+matrix_title[chunks]
            matrices.to_pickle(savepath+'\\'+new_matrix_title+'.pkl')
        return(matrices)
    else:
        matrices=[]
        for m in range(len(indexes)-1):
            b=indexes[m]+1
            if m == len(indexes)-1:
                a=len(matrix)
            else:
                a=indexes[m+1]
            matrices.append(matrix.iloc[b:a])
            matrices[m] = matrices[m]['Column1'].str.split(" ", n = 2, expand = True)
            matrices[m].columns = ['Origin','Destination','km']
            matrices[m].Destination=matrices[m].Destination.str[:-1]
            matrices[m][['Origin', 'Destination', 'km']]=matrices[m][['Origin', 'Destination', 'Km']].apply(to_numeric)
            if save == True:
                matrix_title=str(matrix.iloc[indexes[m:m+1]].values[0])[15:-2]
                matrix_title=matrix_title.replace(", ", " ")
                matrix_title=matrix_title.split()
                for chunks in range(len(matrix_title)):
                    if chunks == 0 or chunks == 1:
                        continue
                    if chunks == 2:
                        new_matrix_title=matrix_title[chunks]
                    else:    
                        new_matrix_title=new_matrix_title+'_'+matrix_title[chunks]
                matrices[m].to_pickle(savepath+'\\'+new_matrix_title+'.pkl')
        return(matrices)
class UFS:
    def __init__(self, name,PATH="C:/SATWIN/XEXES_11.3.12W_MC"):
        self.name=name
        self.path=PATH
    def actual_flow(self,PATH ="",file="",by_userclass="",Clean_up = True,Coordinates=True,Output=False):
        import pandas as pd
        from os import system, remove
        import time
        Data=[24]
        if PATH=="":
            PATH=self.path
        stamp=str(round(time.time()/3333))
        UFS1=self.name.replace("/","\\\\")
        UFS1=self.name.replace(".ufs","")
        UFS1=self.name.replace(".UFS","")
        UFS1n=UFS1.split('\\')[-1]
        UFS1p=UFS1.replace(UFS1n,"")
        if file=="":
            file=UFS1n+stamp+".csv"
        if by_userclass!='':
            for UC in range(by_userclass):
                Data.append('40U'+str(UC+1))
        comands = list(map(lambda x: str(x) +"; ", Data))
        text= "SET PATH="+PATH+"\nP1X "+ "'" + UFS1+ "'" +"/DUMP " + file +"; " +"".join(comands)
        f = open(stamp+"P1X_DUMP.bat","w+")
        f.write(text)
        f.close()
        system(stamp+"P1X_DUMP.bat")
        remove(stamp+"P1X_DUMP.bat")
        keyfile="           6                                                                7025\n"+"           6                                                                7100\n"+"           0                                                                7100\n"+"          13                                                                7025\n"+"           1                                                                7530\n"+"           0                                                                7530\n"+UFS1n+stamp+"_Coord.csv\n"+"           0                                                                7025\n"+"y                                                                           9200\n"
        f = open(UFS1p+stamp+"temp_coor.key","w+")
        f.write(keyfile)
        f.close()
        text= PATH+"\$SATDB " + "'" + UFS1+ "'" +" Key "+ "'"+UFS1p+stamp +"temp_coor.key' " + "VDU vdu"
        f = open(stamp+"SATDB_Coord.bat","w+")
        f.write(text)
        f.close()
        system(stamp+"SATDB_Coord.bat")
        remove(stamp+"SATDB_Coord.bat")
        remove(UFS1p+stamp+"temp_coor.key")
        names=['A_Node','B_Node','C_Node', 'Total_Actual_flow']
        if by_userclass!='':
            for UC in range(by_userclass):
                names.append('UC'+str(UC+1))
        df=pd.read_csv(file,index_col=None, header=None, names=names, dtype={'A_Node':'str','B_Node':'str','C_Node':'str'})
        df['C_Node']=df.C_Node.astype('str')
        if Coordinates:
            coord=pd.read_csv(UFS1n+stamp+"_Coord.csv",index_col=None, header=None, names=['A_Node','B_Node','C_Node', 'X1', 'Y1','X2','Y2'],dtype={'A_Node':'str','B_Node':'str','C_Node':'str'})
            coord['C_Node']=coord.C_Node.astype('str')
            df=pd.merge(df, coord, on=['A_Node','B_Node','C_Node'], how='left')
        if Output:
            df.to_csv(UFS1 +"_Act_Flows.csv",index=False)
        if Clean_up & Coordinates:
            remove(UFS1n+stamp+"_Coord.csv")
            remove(file)
            remove(UFS1+".LPD")
            remove(UFS1+".LPP")
            remove("vdu.VDU")
            remove("DUMMY.VDU")
        return df
    def p1x_dump(self,PATH ="",file="",Data="",Clean_up = True,Coordinates=True,Output=False):
        import pandas as pd
        from os import system, remove
        import time
        if PATH=="":
            PATH=self.path
        stamp=str(round(time.time()/3333))
        UFS1=self.name.replace("/","\\\\")
        UFS1=self.name.replace(".ufs","")
        UFS1=self.name.replace(".UFS","")
        UFS1n=UFS1.split('\\')[-1]
        UFS1p=UFS1.replace(UFS1n,"")
        if file=="":
            file=UFS1n+stamp+".csv"
        comands = list(map(lambda x: str(x) +"; ", Data))
        text= "SET PATH="+PATH+"\nP1X " + "'" + UFS1+ "'" +"/DUMP " + file +"; " +"".join(comands)
        f = open(stamp+"P1X_DUMP.bat","w+")
        f.write(text)
        f.close()
        system(stamp+"P1X_DUMP.bat")
        remove(stamp+"P1X_DUMP.bat")
        keyfile="           6                                                                7025\n"+"           6                                                                7100\n"+"           0                                                                7100\n"+"          13                                                                7025\n"+"           1                                                                7530\n"+"           0                                                                7530\n"+UFS1n+stamp+"_Coord.csv\n"+"           0                                                                7025\n"+"y                                                                           9200\n"
        f = open(UFS1p+stamp+"temp_coor.key","w+")
        f.write(keyfile)
        f.close()
        text= PATH+"\$SATDB " + "'" + UFS1+ "'" +" Key "+ "'"+UFS1p+stamp +"temp_coor.key' " + "VDU vdu"
        f = open(stamp+"SATDB_Coord.bat","w+")
        f.write(text)
        f.close()
        system(stamp+"SATDB_Coord.bat")
        remove(stamp+"SATDB_Coord.bat")
        remove(stamp+"temp_coor.key")
        names=['A_Node','B_Node','C_Node']
        for D in range(len(Data)):
            names.append('DATA_'+str(Data[D]))
        df=pd.read_csv(file,index_col=None, header=None, names=names, dtype={'A_Node':'str','B_Node':'str','C_Node':'str'})
        df['C_Node']=df.C_Node.astype('str')
        if Coordinates:
            coord=pd.read_csv(UFS1n+stamp+"_Coord.csv",index_col=None, header=None, names=['A_Node','B_Node','C_Node', 'X1', 'Y1','X2','Y2'],dtype={'A_Node':'str','B_Node':'str','C_Node':'str'})
            coord['C_Node']=coord.C_Node.astype('str')
            df=pd.merge(df, coord, on=['A_Node','B_Node','C_Node'], how='left')
        if Output:
            df.to_csv(UFS1 + "_Data.csv",index=False)
        if Clean_up:
            remove(UFS1n+stamp+"_Coord.csv")
            remove(file)
            remove(UFS1+".LPD")
            remove(UFS1+".LPP")
            remove("vdu.VDU")
            remove("DUMMY.VDU")
        return df
    def plot_flows(self,PATH="",UFS2="",func='y-x',by_userclass="",location=[51.704740, -0.042465],html='',scale=2000):
        import pandas as pd
        from pyproj import Proj, transform
        import folium
        from folium import plugins
        import numpy as np
        if PATH=="":
            PATH=self.path
        df=self.actual_flow(by_userclass=by_userclass)
        UFS2=UFS2.replace("/","\\\\")
        UFS2=UFS2.replace(".ufs","")
        UFS2=UFS2.replace(".UFS","")
        if UFS2 !='':
            UFS2=UFS(UFS2)
            df2=UFS2.actual_flow(by_userclass=by_userclass, Coordinates=False)
            df=pd.merge(df, df2, on=['A_Node','B_Node','C_Node'], how='left')
        UFS1=self.name.replace("/","\\\\")
        UFS1=self.name.replace(".ufs","")
        UFS1=self.name.replace(".UFS","")
        if html =='':
            html=UFS1.split('\\')[-1]
        ###
        inProj = Proj(init='epsg:27700')
        outProj = Proj(init='epsg:4326')
        def ColstoCol(a,b,c,d):
            a, b =transform(inProj,outProj,a,b)
            c, d =transform(inProj,outProj,c,d)
            return[[b,a],[d,c]]
        df['link']=np.vectorize(ColstoCol, otypes=[list])(df.X1,df.Y1,df.X2,df.Y2)
        ###
        m=folium.Map(crs='EPSG3857',location=location,zoom_start=9,weight=0.2,tiles='cartodbpositron')
        net = folium.FeatureGroup(name='network')
        m.add_child(net)
        folium.PolyLine(locations=df['link'],color="black",weight=0.25).add_to(net)
        fg = folium.FeatureGroup(name='Flows')
        m.add_child(fg)
        Af_uc = plugins.FeatureGroupSubGroup(fg,'Total_flow')
        m.add_child(Af_uc)
        if UFS2 !='':
            def g(latlong,flow1,flow2,f):
                flow=f(flow1,flow2)
                if flow!=0:
                    color='green'
                    if flow<0:
                        color='blue'
                        flow=-flow
                    return plugins.PolyLineOffset(locations=latlong,color=color,offset=-abs(flow)/scale/2-1.5,tooltip='PCUs: '+str(round(flow,2)),weight=flow/scale).add_to(Af_uc)
            def f(x,y):
                return eval(func)
            np.vectorize(g,excluded=['f'])(df.link,df.Total_Actual_flow_x,df.Total_Actual_flow_y,f)
        else:
            def g(latlong,flow):
                return plugins.PolyLineOffset(locations=latlong,color='green',offset=-abs(flow)/scale/2-1.5,tooltip='PCUs: '+str(round(flow,2)),weight=flow/scale).add_to(Af_uc)
            np.vectorize(g)(df.link,df.Total_Actual_flow)
        if UFS2 !='':
            if by_userclass!='':
                for UC in range(by_userclass):
                    Af_uc = plugins.FeatureGroupSubGroup(fg,'UC'+str(UC+1))
                    m.add_child(Af_uc)
                    def g(latlong,flow1,flow2,f):
                        flow=f(flow1,flow2)
                        color='green'
                        if flow<0:
                            color='blue'
                        return plugins.PolyLineOffset(locations=latlong,color=color,offset=-abs(flow)/scale/2-1.5,tooltip='PCUs: '+str(round(flow,2)),weight=flow/scale).add_to(Af_uc)
                    def f(x,y):
                        return eval(func)
                    np.vectorize(g,excluded=['f'])(df.link,df['UC'+str(UC+1)+'_x'],df['UC'+str(UC+1)+'_y'],f)
        else:
            if by_userclass!='':
                for UC in range(by_userclass):
                    Af_uc = plugins.FeatureGroupSubGroup(fg,'UC'+str(UC+1))
                    m.add_child(Af_uc)
                    def g(latlong,flow):
                        return plugins.PolyLineOffset(locations=latlong,color='green',offset=-abs(flow)/scale/2-1.5,tooltip='PCUs: '+str(round(flow,2)),weight=flow/scale).add_to(Af_uc)
                    np.vectorize(g)(df.link,df['UC'+str(UC+1)])
        folium.LayerControl(collapsed=False).add_to(m)
        return m.save(html+'.html')
    def plot_Data(self,Data="",PATH="",UFS2="",func='y-x',location=[51.704740, -0.042465],html='',scale=2000):
        import pandas as pd
        from pyproj import Proj, transform
        import folium
        from folium import plugins
        import numpy as np
        if PATH=="":
            PATH=self.path
        df=self.P1X_Dump(Data=Data)
        UFS2=UFS2.replace("/","\\\\")
        UFS2=UFS2.replace(".ufs","")
        UFS2=UFS2.replace(".UFS","")
        if UFS2 !='':
            UFS2=UFS(UFS2)
            df2=UFS2.P1X_Dump(Data=Data, Coordinates=False)
            df=pd.merge(df, df2, on=['A_Node','B_Node','C_Node'], how='left')
        UFS1=self.name.replace("/","\\\\")
        UFS1=self.name.replace(".ufs","")
        UFS1=self.name.replace(".UFS","")
        if html =='':
            html=UFS1.split('\\')[-1]
        ###
        inProj = Proj(init='epsg:27700')
        outProj = Proj(init='epsg:4326')
        def ColstoCol(a,b,c,d):
            a, b =transform(inProj,outProj,a,b)
            c, d =transform(inProj,outProj,c,d)
            return[[b,a],[d,c]]
        df['link']=np.vectorize(ColstoCol, otypes=[list])(df.X1,df.Y1,df.X2,df.Y2)
        ###
        m=folium.Map(crs='EPSG3857',location=location,zoom_start=9,weight=0.2,tiles='cartodbpositron')
        net = folium.FeatureGroup(name='network')
        m.add_child(net)
        folium.PolyLine(locations=df['link'],color="black",weight=0.25).add_to(net)
        fg = folium.FeatureGroup(name='Data')
        m.add_child(fg)
        if len(Data)==1:
            Af_uc = plugins.FeatureGroupSubGroup(fg,Data)
            m.add_child(Af_uc)
            if UFS2 !='':
                def g(latlong,flow1,flow2,f):
                    flow=f(flow1,flow2)
                    if flow!=0:
                        color='green'
                        if flow<0:
                            color='blue'
                            flow=-flow
                        return plugins.PolyLineOffset(locations=latlong,color=color,offset=-abs(flow)/scale/2-1.5,tooltip='PCUs: '+str(round(flow,2)),weight=flow/scale).add_to(Af_uc)
                def f(x,y):
                    return eval(func)
                np.vectorize(g,excluded=['f'])(df.link,df['DATA'+'_x'],df['DATA'+'_y'],f)
            else:
                def g(latlong,flow):
                    return plugins.PolyLineOffset(locations=latlong,color='green',offset=-abs(flow)/scale/2-1.5,tooltip='PCUs: '+str(round(flow,2)),weight=flow/scale).add_to(Af_uc)
                np.vectorize(g)(df.link,df[Data])
        else:
            if UFS2 !='':
                for UC in Data:
                    Af_uc = plugins.FeatureGroupSubGroup(fg,'DATA_'+str(UC))
                    m.add_child(Af_uc)
                    def g(latlong,flow1,flow2,f):
                        flow=f(flow1,flow2)
                        color='green'
                        if flow<0:
                            color='blue'
                        return plugins.PolyLineOffset(locations=latlong,color=color,offset=-abs(flow)/scale/2-1.5,tooltip='PCUs: '+str(round(flow,2)),weight=flow/scale).add_to(Af_uc)
                    def f(x,y):
                        return eval(func)
                    np.vectorize(g,excluded=['f'])(df.link,df['DATA_'+str(UC)+'_x'],df['DATA_'+str(UC)+'_y'],f)
            else:
                for UC in range(Data):
                    Af_uc = plugins.FeatureGroupSubGroup(fg,str(UC))
                    m.add_child(Af_uc)
                    def g(latlong,flow):
                        return plugins.PolyLineOffset(locations=latlong,color='green',offset=-abs(flow)/scale/2-1.5,tooltip='PCUs: '+str(round(flow,2)),weight=flow/scale).add_to(Af_uc)
                    np.vectorize(g)(df.link,df['DATA_'+str(UC)])
        folium.LayerControl(collapsed=False).add_to(m)
        return m.save(html+'.html')