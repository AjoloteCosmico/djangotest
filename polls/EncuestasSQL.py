from pickle import FALSE
import mysql.connector
import pandas as pd
class EncuestasDB:
    cnx = mysql.connector.connect(user='fgonzalez', password='6bM59%1**t^O',
                              host='192.168.0.254',
                              database='encuesta',
                              use_pure=False)
    encuestas = pd.DataFrame()
    encuestasIncompletas=pd.DataFrame()
    Eg2019 =    pd.DataFrame()
    listado_carreras=pd.DataFrame
    listado_planteles=pd.DataFrame
    @staticmethod    
    def formatear_cuenta(columna):
        """ Formatea los números de cuenta para que tengan un formato consistente y comparable

         Parámetros
        ----------
        columna : DataFrame / list / Series
            Números de cuenta

        Devuelve
        -------
        Series
            Números de cuenta formateados
        """
        # Copiar la columna para no sobreescribirla
        columna = columna.copy()
        # Convertir la columna a tipo Series de pandas
        columna = pd.Series(columna)
        # Convertir a tipo string
        columna = columna.astype('str')
        # Remplazar todo lo que no es número con la cadena vacía
        columna = columna.str.replace("\D", "", regex = True)
        # Llenar las cadenas con ceros a la izquierda para que tengan todas 9 dígitos
        columna = columna.str.pad(width=9, side='left', fillchar='0')
    
        return columna    
    
    #TODO: dgae como dataframe debera en un futuro ser un parametro, al igual que la generacion
    #Eg2019 pasará a llamarse EgGeneracion
    def __init__(self):
        self.cnx.commit()
        #Todas las encuestas alv, elegir NBR7 también 
        query = ('SELECT cuenta, aplica, fec_capt, nbr7,ngr11f FROM respuestas2  order by fec_capt ')
        self.encuestas=pd.read_sql(query,self.cnx)

        # Formatear cuenta
        self.encuestas['cuenta'] = EncuestasDB.formatear_cuenta(self.encuestas['cuenta'])
        dgae = pd.read_excel('dgae.xlsx')
         #Seleccionamos unicamente a los egresados de 2019, que son el objetivo de este estudio
        self.Eg2019 = dgae.loc[dgae["ANIO"]==2019,['CUENTA', 'PLANTEL', 'CARRERA']]
        # Formateo de cuenta
        self.Eg2019['CUENTA'] = EncuestasDB.formatear_cuenta(self.Eg2019['CUENTA'])
        # Renombre de columna
        self.Eg2019.rename(columns={"CUENTA":"cuenta"}, inplace=True)
        #Para que coincida con nuestras bases modificamos las claves de estos planteles a la centena cerrada.
        for i in range(1,8) :
            self.Eg2019.loc[(self.Eg2019["PLANTEL"]>i*100)&(self.Eg2019["PLANTEL"]<(i+1)*100),"PLANTEL"]=i*100
        # Hacer el merge left (encuestas2019 es más chiquito, entonces lo pongo a la izquierda)
        encuestas_mezcla = self.encuestas.merge(self.Eg2019, on='cuenta', how='left')
        encuestas2019_conMatch = encuestas_mezcla[encuestas_mezcla['PLANTEL'].notna()] 
        #En adelante, contamos solo encuestas completas, unu
        self.encuestas=encuestas2019_conMatch.loc[encuestas2019_conMatch["ngr11f"].notna()]
        self.encuestasIncompletas=encuestas2019_conMatch.loc[encuestas2019_conMatch["ngr11f"].isna()]
        self.listado_carreras = pd.read_excel(r'files/Listado de carreras y planteles actualizados-27-06-2022.xlsx',usecols=[2,3], names=('Clave Carrera', "Carrera")).drop_duplicates() 
        self.listado_planteles = pd.read_excel(r'files/Listado de carreras y planteles actualizados-27-06-2022.xlsx',usecols=[0,1], names=('Clave Plantel', "Plantel")).drop_duplicates()
        print(" EncuestasDB del PVE Comit 1.2.5")



    def carrera(self,clave):
        Scarrera=str(self.listado_carreras.loc[self.listado_carreras["Clave Carrera"]==clave,"Carrera"].values[0])
            #return(unidecode.unidecode(Scarrera.upper()))
        return Scarrera

    
    def plantel(self,clave):
        Splantel=str(self.listado_planteles.loc[self.listado_planteles["Clave Plantel"]==clave,"Plantel"].values[0])
            #return(unidecode.unidecode(Splantel.upper()))
        return Splantel


    def cuentaPorEncuestador(self,fechaInicial=None):
        df = self.encuestas
        if fechaInicial:
            df = df[df['fec_capt'] > fechaInicial]
        ClavesNombres = {'17': 'Erendira', '12':'Mónica', '15':'César', '20':'María', '21':'Ivonne'}
        contador = {k:0 for k in ClavesNombres.keys()}
        contador['20'] += 39
        contador['21'] += 38
        for i in df["aplica"]:
            if i in ClavesNombres.keys():
                contador[i] += 1
        contador = pd.DataFrame([[ClavesNombres[k],contador[k]] for k in contador.keys()], columns=['Encuestador', 'Realizadas'])
        return contador
    
    def cuentaPorMes(self,fechaInicial=None):
        import warnings
        def fxn():
           warnings.warn("deprecated", DeprecationWarning)

        with warnings.catch_warnings():
             warnings.simplefilter("ignore")
             fxn()
        Meses = {'01': 'Enero', '02':'Febrero', '03':'Marzo', '04':'Abril', '05':'Mayo','06': 'Mayo',
                   '07': 'Julio', '08':'Agosto', '09':'Septiembre', '10':'Octubre', '11':'Noviembre', '12':'Diciembre'}
        df = self.encuestas
        if fechaInicial:
            df = df[df['fec_capt'] > fechaInicial]
        conteo=pd.DataFrame(columns=["Mes","realizadas"])
        contador = df.groupby(df['fec_capt'].dt.strftime('%Y-%m'))['cuenta'].count()
        sinFecha = len(df) - contador.sum()
        contador = pd.DataFrame(contador)
        for i in contador.itertuples():
            conteo=conteo.append({"Mes": Meses[i[0][5:7]]+" "+i[0][0:4],
                              "realizadas": i[1]
                              },ignore_index=True)
        
        #conteo=conteo.append({"Mes": "Sin fecha","realizadas": sinFecha},ignore_index=True)
        return conteo
    
    def cuentaPorCarrera(self,fechaInicial=None):
        import warnings

        def fxn():
           warnings.warn("deprecated", DeprecationWarning)

        with warnings.catch_warnings():
             warnings.simplefilter("ignore")
             fxn()
        df = self.encuestas
        telefonicas=df[df['aplica'].notna()]
        porInternet=df[df['aplica'].isna()]
        conteo=pd.DataFrame(columns=["ClaveCarrera","ClavePlantel","Internet","Telefonicas"])
        if fechaInicial:
            df = df[df['fec_capt'] > fechaInicial]
    
        for i in self.Eg2019["PLANTEL"].unique():
           for k in self.Eg2019.loc[self.Eg2019["PLANTEL"]==i,"CARRERA"].unique():
               conteo=conteo.append({
                "ClaveCarrera": k,
                "ClavePlantel":i,
                "Internet": porInternet.loc[(porInternet["PLANTEL"]==i)&(porInternet["CARRERA"]==k),"cuenta"].size,
                "Telefonicas": telefonicas.loc[(telefonicas["PLANTEL"]==i)&(telefonicas["CARRERA"]==k),"cuenta"].size,
               },ignore_index=True)
        return conteo

    def repIndividual(self):
        reporte=pd.DataFrame(columns=["cuenta","Aplicador","PLANTEL","CARRERA","Fecha"])
        print("Actualized")
        for i in self.encuestas.itertuples():
            aplicador=i[2]
            if(pd.isna(i[2])):
                aplicador="Internet"
            fecha=i[3]
            if(pd.isna(i[3])):
                fecha="Encuesta incompleta"
            reporte=reporte.append({
                "cuenta": i[1],
                "Aplicador":aplicador,
                "PLANTEL":self.plantel(i[5]),
                "CARRERA":self.carrera(i[6]),
                "Fecha": fecha
            }, ignore_index=True)

        return reporte