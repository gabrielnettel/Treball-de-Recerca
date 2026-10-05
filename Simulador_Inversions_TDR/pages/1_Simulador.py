# LLIBRERIES
# S'importa la llibreria Streamlit, necessària per crear la interfície de l'aplicació
import streamlit as st
# https://docs.streamlit.io/get-started/installation

# S'importa datetime per treballar amb dates
import datetime# per la data
# https://www.w3schools.com/python/python_datetime.asp 

# S'importa yfinance per obtenir dades històriques dels actius financers
import yfinance as yh 
# https://pypi.org/project/yfinance/

# S'importa pandas per treballar i organitzar les dades en estructures tabulars
import pandas as pd
# https://pandas.pydata.org/docs/getting_started/install.html

# S'importa Altair per crear gràfics a partir de les dades obtingudes
import altair as alt
# https://altair-viz.github.io/getting_started/installation.html



# CONFIGURACIÓ DE LA PÀGINA
# Es configura la pàgina perquè els elements es distribueixin aprofitant tota l'amplada disponible
st.set_page_config(layout="wide")
# https://docs.streamlit.io/develop/api-reference/configuration/st.set_page_config 


# INICIALITZACIÓ DE LES VARIABLES DE SESSIÓ
# Es comprova si existeix la variable "simulació_realitzada" dins de session_state i, si no existeix, se li assigna el valor False
if "simulació_realitzada" not in st.session_state: 
    st.session_state.simulació_realitzada = False
    # https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state 

# Es comprova si existeix la variable "boto_començar" i, si no existeix, se li assigna el valor False       
if "boto_començar" not in st.session_state: #és ST. session"_"state
 st.session_state.boto_començar=False

# Es comprova si existeix la llista de simulacions guardades i, si no existeix, es crea una llista buida
if "simulacions_guardades" not in st.session_state:
    st.session_state.simulacions_guardades = []

    

# BARRA LATERAL I SIMULACIONS GUARDADES
# Es crea una barra lateral per mostrar el nombre de simulacions guardades
with st.sidebar:
#https://docs.streamlit.io/develop/api-reference/layout/st.sidebar

    espais_laterals=16
    for i in range(espais_laterals):
    # https://www.geeksforgeeks.org/python/python-range-function/

        st.title(" ")
    # https://docs.streamlit.io/develop/api-reference/text/st.title
  
    # Es mostra el títol de l'apartat de simulacions guardades
    st.subheader("Simulacions guardades")
    #https://docs.streamlit.io/develop/api-reference/text/st.subheader 

    # Es mostra el nombre de simulacions que hi ha actualment a la llista
    st.metric(
        label="Simulacions guardades",
        value= len(st.session_state.simulacions_guardades), 
        #https://www.w3schools.com/python/ref_func_len.asp
        label_visibility="collapsed")
    # https://docs.streamlit.io/develop/api-reference/data/st.metric 
    


# DICCIONARI D'EMPRESES I TICKERS
# Es crea un diccionari que relaciona el nom de cada empresa amb el seu ticker de Yahoo Finance
diccionari_tickers= {
      
    # Tecnologia
    "Apple": "AAPL","Microsoft": "MSFT","Nvidia": "NVDA","TSMC": "TSM","Adobe": "ADBE",

    # Financer
    "JPMorgan Chase": "JPM","Goldman Sachs": "GS","American Express": "AXP","Visa": "V","Mastercard": "MA",

    # Serveis digitals
    "Amazon": "AMZN","eBay": "EBAY","Booking Holdings": "BKNG","Cisco Systems": "CSCO","Alphabet": "GOOG",

    # Energia
    "ExxonMobil": "XOM","Chevron": "CVX","NextEra Energy": "NEE","AES": "AES","EQT": "EQT",

    # Salut
    "UnitedHealth Group": "UNH","McKesson": "MCK","CVS Health": "CVS","Amgen": "AMGN","Pfizer": "PFE",

    # Inmobiliari
    "D.R. Horton": "DHI","Lennar": "LEN","Hovnanian Enterprises": "HOV","PulteGroup": "PHM","Toll Brothers": "TOL",

    # Automoció
    "Volkswagen": "VWAGY","Toyota": "TM","PACCAR": "PCAR","Ford": "F","Honda": "HMC",

    # Consum
    "Walmart": "WMT","Nestlé": "NSRGY","Coca-Cola": "KO","PepsiCo": "PEP","Procter & Gamble": "PG",
    }
# https://www.w3schools.com/python/python_dictionaries.asp 


# TÍTOL DEL SIMULADOR
# Es mostra el títol principal del simulador
st.title("SIMULADOR D'INVERSIONS")


# ETAPA 1: CONFIGURACIÓ DE LA INVERSIÓ
# Es mostra el títol corresponent a la primera etapa
st.subheader("Etapa 1")


# DADES DE LA INVERSIÓ
# Es divideix l'espai disponible en dues columnes per distribuir les dades de la inversió
col1,col2=st.columns(2)
# https://docs.streamlit.io/develop/api-reference/layout/st.columns

# Es treballa dins de la primera columna, on es demanen les dades inicials de la simulació
with col1:

    # Es crea un contenidor amb una vora per agrupar visualment les dades de la inversió
    with st.container(border=True):
    #https://docs.streamlit.io/develop/api-reference/layout/st.container

        # Es mostra el títol de l'apartat de dades
        st.header("Dades de la inversió")
        # https://docs.streamlit.io/develop/api-reference/text/st.header

        # SELECCIÓ DEL CAPITAL INICIAL
        # Es demana el capital inicial mitjançant una barra lliscant
        # El valor inicial és de 15.000 $ i el capital es pot modificar en intervals de 100 $
        capital_inicial = st.slider(
            label = "Introdueix el capital inicial en $:",
            min_value= 100,
            max_value=50000,
            value= 15000,
            step=100,   
        )
        # https://docs.streamlit.io/develop/api-reference/widgets/st.slider 
          

        # Es defineix una funció que restableix els estats de la simulació quan es canvia d'estratègia
        def canvi_estratègia():
            st.session_state.simulació_realitzada = False
            st.session_state.Simulació_començada =False
            st.session_state.boto_començar=False
        # https://www.youtube.com/watch?v=oBiuR_Z2ac4&t=11s
           

        # SELECCIÓ DE L'ESTRATÈGIA
        # Es permet seleccionar l'estratègia d'inversió que es vol simular
        estratègia_inversió= st.selectbox(
            label= "Tria l'estratègia",
            options= ["Buy&Hold","Dollar Cost Averaging(DCA)","Stop-Loss i Take-Profit","Diversificació"],
            # https://www.w3schools.com/python/python_lists.asp

            # Cada vegada que es modifica l'estratègia, s'executa la funció canvi_estratègia
            on_change= canvi_estratègia # Anotació: No hi ha cap parèntesis
            )
        # https://docs.streamlit.io/develop/api-reference/widgets/st.selectbox


        # Es defineix una funció que restableix els estats de la simulació quan es canvia de sector
        def canvi_sector():
             st.session_state.simulació_realitzada=False
             st.session_state.Simulació_començada = False
             st.session_state.boto_començar=False


        # Si l'estratègia no és Diversificació, es permet seleccionar una única empresa
        if estratègia_inversió != "Diversificació": 
        # https://www.geeksforgeeks.org/python/python-not-equal-operator/

            

            # SELECCIÓ DEL SECTOR I DE L'EMPRESA
            # Es permet seleccionar el sector en què es vol invertir
            sector_seleccionat= st.selectbox( 
                label ="Tria el sector",
                options =["Tecnologia","Financer","Serveis digitals","Energia","Salut","Inmobiliari","Automoció","Consum"],# ha de ser options sí o sí
                on_change=canvi_sector
            )


            # Es defineix una funció que restableix els estats de la simulació quan es canvia d'empresa
            def canvi_empresa():
                 st.session_state.simulació_realitzada=False
                 st.session_state.Simulació_començada=False   
                 st.session_state.boto_començar=False# divers
            

            # Es mostra una llista d'empreses diferent segons el sector seleccionat
            if sector_seleccionat == "Tecnologia":
            # https://stackoverflow.com/questions/35857752/what-do-the-symbols-and-mean-in-python-when-is-each-used

                empresa_seleccionada = st.selectbox( 
                    label ="Tria l'empresa", # Jo prefereixo sempre posar label perquè així és més polit(no és necessari)
                    options = ["Apple", "Microsoft","Nvidia","TSMC","Adobe"],
                    on_change=canvi_empresa
                )
            

            elif sector_seleccionat == "Financer":
            # https://www.freecodecamp.org/espanol/news/sentencias-if-elif-y-else-en-python/

                empresa_seleccionada= st.selectbox(
                label = "Tria l'empresa",
                options=["JPMorgan Chase","Goldman Sachs","American Express","Visa","Mastercard"],
                on_change=canvi_empresa
                )

            elif sector_seleccionat == "Serveis digitals":
                empresa_seleccionada = st.selectbox(
                label = "Tria l'empresa",
                options=["Amazon","eBay","Booking Holdings","Cisco Systems","Alphabet"],
                on_change=canvi_empresa
                )

            elif sector_seleccionat == "Energia":
                empresa_seleccionada = st.selectbox(
                label = "Tria l'empresa",
                options=["ExxonMobil","Chevron","NextEra Energy","AES","EQT"],
                on_change=canvi_empresa
                )

            elif sector_seleccionat == "Salut":
                empresa_seleccionada = st.selectbox(
                label = "Tria l'empresa",
                options=["UnitedHealth Group","McKesson","CVS Health","Amgen","Pfizer"],
                on_change=canvi_empresa
                )

            elif sector_seleccionat == "Inmobiliari":
                empresa_seleccionada = st.selectbox(
                label = "Tria l'empresa",
                options=["D.R. Horton","Lennar","Hovnanian Enterprises","PulteGroup","Toll Brothers"],
                on_change=canvi_empresa
                )

            elif sector_seleccionat == "Automoció":
                empresa_seleccionada = st.selectbox(
                label = "Tria l'empresa",
                options=["Volkswagen","Toyota","PACCAR","Ford","Honda"],
                on_change=canvi_empresa
                )
           
            elif sector_seleccionat == "Consum":
                empresa_seleccionada = st.selectbox(
                label = "Tria l'empresa",
                options=["Walmart","Nestlé","Coca-Cola","PepsiCo","Procter&Gamble"],
                on_change=canvi_empresa
                )
           


        # Si l'estratègia no és Diversificació, es treballa amb una única empresa
        if estratègia_inversió != "Diversificació":


                    # OBTENCIÓ DE LES DADES HISTÒRIQUES
                    # Es busca el ticker corresponent a l'empresa seleccionada dins del diccionari
                    ticker=diccionari_tickers[empresa_seleccionada]
                    # https://www.w3schools.com/python/python_dictionaries_access.asp

                    # Es crea un objecte de Yahoo Finance associat al ticker seleccionat
                    empresa_financera= yh.Ticker(ticker)
                    # https://youtu.be/j0sBKAB75oc?si=5Em2JI4wpwI6HtXy

                    # S'obté tot l'historial disponible de l'empresa per determinar la primera data amb dades
                    historial_empresa=empresa_financera.history(period="max")
                    # https://ranaroussi.github.io/yfinance/reference/api/yfinance.download.html

                    # SELECCIÓ DEL PERÍODE DE LA SIMULACIÓ
                    # Es demana la data inicial de la inversió
                    data_1= st.date_input(
                    # https://docs.streamlit.io/develop/api-reference/widgets/st.date_input
                        label="Tria la data d'inici",   

                        # Es transforma la primera data disponible en un objecte date
                        value= historial_empresa.index[0].to_pydatetime().date(),
                        # https://www.ionos.com/digitalguide/websites/web-development/python-pandas-dataframe-indexing/
                        # https://pandas.pydata.org/docs/reference/api/pandas.Timestamp.to_pydatetime.html
                        # https://docs.python.org/es/3/library/datetime.html#datetime.date

                        # La data inicial no pot ser anterior a la primera data amb dades disponibles
                        min_value=historial_empresa.index[0].to_pydatetime().date(),

                         # La data màxima permesa és la data actual
                        max_value=datetime.date.today()
                        # https://docs.python.org/es/3.8/library/datetime.html
                        )
                    
                    # Es demana la data final de la simulació
                    data_final=st.date_input(
                        label="Tria la data final",
                        value=datetime.date.today(),
                        min_value=historial_empresa.index[0].to_pydatetime().date(),
                        max_value=datetime.date.today()
                    )
                    # Es comprova que la data final sigui posterior a la data inicial
                    if data_final<=data_1:
                    # https://www.geeksforgeeks.org/python/comparing-dates-python/
                                st.write("La data inicial no pot ser superior a la de inici")
                                # https://docs.streamlit.io/develop/api-reference/write-magic/st.write
                    
                    # Si les dates són correctes, s'obtenen les dades corresponents al període seleccionat
                    else:
                            dades_simulació= empresa_financera.history(
                                # Es limita l'historial a les dates seleccionades
                                start=data_1,
                                end= data_final + datetime.timedelta(days=1),
                                auto_adjust=True
                                )
                            # https://algotrading101.com/learn/yfinance-guide/

                            # Es comprova si s'han obtingut dades per al període seleccionat
                            if dades_simulació.empty:
                            # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.empty.html
                                    st.write("No hi ha dades disponibles per a aquestes dates")

                            
                            else:   
                                    # S'obté el preu d'obertura del primer dia disponible
                                    preu_obertura_inicial = dades_simulació["Open"].iloc[0]  

                                    # S'obté el preu de tancament de l'últim dia disponible
                                    preu_tancament_final = dades_simulació["Close"].iloc[-1]
                                    # https://pandas.pydata.org/docs/getting_started/intro_tutorials/03_subset_data.html
                                    # https://medium.com/@icodewithben/understanding-the-iloc-function-in-pandas-da9dec1a1ee1

        # Si l'estratègia és Diversificació, es demanen unes dates comunes per a totes les empreses                     
        else:
              # Es demana la data inicial de la simulació
              data_inici_diversificació=st.date_input(
              
                   label="Tria la data de inici",
                   value=datetime.date(2000,1,1),
                   min_value=datetime.date(1900,1,1),
                   max_value=datetime.date(2026,1,1)
                   )

              # Es demana la data final de la simulació
              data_final_diversificació=st.date_input(
                            
                    label="Tria la data de final",
                    value=datetime.date.today(),
                    min_value=datetime.date(1990,1,1),
                    max_value=datetime.date.today()
                    )
              
              # Es comprova que la data final sigui posterior a la data inicia
              if data_final_diversificació<=data_inici_diversificació:
                    st.write("La data inicial no pot ser superior a la de inici")

              

        # Es defineix una funció que reinicia l'estat de la simulació quan es modifica la freqüència del DCA
        def canvi_mensual_anual():
                st.session_state.simulació_realitzada=False
                

        # CONFIGURACIÓ DEL DCA
        # Si l'estratègia seleccionada és Dollar Cost Averaging, es determina la freqüència de les aportacions
        if estratègia_inversió== "Dollar Cost Averaging(DCA)":
                            
                            # Es calcula la diferència entre les dates en mesos
                            nombre_mesos = (data_final.year * 12+ data_final.month)-(data_1.year*12+ data_1.month)
                            # https://es.stackoverflow.com/questions/513244/como-calcular-el-numero-de-meses-entre-dos-fechas
                            # https://docs.python.org/3/library/datetime.html

                            # Si el període és de dos anys o més, es permet escollir entre freqüència mensual i anual
                            if nombre_mesos >=24:
                                    freqüència_DCA = st.selectbox(
                                    label="Tria la freqüència:",
                                    options= ["Mensual","Anual"],
                                    on_change=canvi_mensual_anual
                                )   
                                     
                            # Si el període és inferior a dos anys, només es permet la freqüència mensual    
                            else: 
                                freqüència_DCA= st.selectbox(
                                    label="Tria la freqüència:",
                                    options=["Mensual"]
                                )

                                # S'informa de la condició necessària per poder seleccionar una freqüència anual
                                st.write("Si desitjes fer-ho anualment el període de temps ha de ser major a 2 anys")

                                # Es reinicia l'estat de la simulació mentre no es compleixi la condició
                                st.session_state.simulació_realitzada=False                          
                                

# INFORMACIÓ DEL SIMULADOR            
# Aquest apartat només té una funció informativa i permet consultar el significat dels diferents elements del simulador
with col2:
    st.subheader("Informació")

    with st.expander("CAPITAL INICIAL"):
    # https://docs.streamlit.io/develop/api-reference/layout/st.expander
        st.write("Quantitat de diners que s'inverteixen al començament de la simulació.")


    with st.expander("SECTOR"):
            st.write("Categoria a la qual pertany l'empresa seleccionada, com ara Tecnologia, Financer, Serveis digitals Energia, Salut, Inmobiliari, Automoció o Consum.")
    
    with st.expander("EMPRESA"):
        st.write("Empresa en la qual es realitza la inversió. Cada empresa està associada a un ticker que permet obtenir les seves dades històriques.")

    with st.expander("PERÍODE DE TEMPS"):
                st.write("Període durant el qual es manté la inversió.")
        
    with st.expander("ESTRATÈGIA"):
            st.write("Mètode utilitzat per gestionar els diners durant la inversió.")

            with st.expander("Buy&Hold"):
                st.write("Consisteix a comprar les accions al començament del període i mantenir-les fins al final de la simulació, sense realitzar noves compres ni vendes.")

            with st.expander("Dollar Cost Averaging(DCA)"):
                st.write("Consisteix a invertir el capital de manera periòdica, realitzant noves aportacions de diners durant el període seleccionat.")
                st.write("**Freqüència**: Indica cada quant de temps es realitza una nova aportació de capital, que pot ser mensual o anual.")


            with st.expander("Stop-Loss i Take-profit"):
                st.write("Permet establir dos límits que poden finalitzar la inversió abans de la data seleccionada.")
                st.write("**Stop-Loss**: És un límit de pèrdua. Si el valor de la inversió baixa fins al percentatge establert, la simulació s'atura.")
                st.write("**Take-Profit**: És un límit de benefici. Si el valor de la inversió puja fins al percentatge establert, la simulació s'atura.")

            with st.expander("Diversificació"):
                st.write("Consisteix a repartir el capital entre diferents empreses per evitar concentrar tota la inversió en una sola companyia.")
                st.write("**Nombre d'empreses**: Indica quantes empreses formaran part de la inversió.")
                st.write("**Percentatge**: Indica quina part del capital total es destina a cada empresa.")

    with st.expander("RESULTATS"):
        st.write("Mostra l'evolució i els principals resultats obtinguts durant la simulació.")

        st.write("**Capital final**: Valor de la inversió al final de la simulació.")

        st.write("**Benefici**: Diferència entre el capital final i el capital invertit.")

        st.write("**Rendibilitat**: Percentatge de guany o pèrdua obtingut respecte del capital invertit.")

        st.write("**Màxim Drawdown**: Major pèrdua percentual acumulada que ha experimentat la inversió respecte del seu màxim anterior.")

        st.write("**Volatilitat**: Mesura de la variació dels rendiments de la inversió. Un valor més elevat indica una major variació.")

        st.write("**Sharpe**: Indicador que relaciona el rendiment obtingut amb la variabilitat de la inversió. Un valor més elevat indica una major rendibilitat en relació amb la volatilitat assumida.")

    with st.expander("GRÀFIC D'EVOLUCIÓ"):
        st.write("Mostra com ha variat el valor de la inversió al llarg del període seleccionat.")
            
    
    
# INICI DE LA SIMULACIÓ        
# Es crea el botó que permet iniciar la simulació i mostrar els resultats
simular_inversió=st.button(
label="Simular inversió")
# https://docs.streamlit.io/develop/api-reference/widgets/st.button

# Quan es prem el botó, s'actualitza l'estat de la simulació
if simular_inversió == True:
      st.session_state.simulació_realitzada = True
      
# Si la simulació s'ha iniciat, es procedeix a calcular i mostrar els resultats
if st.session_state.simulació_realitzada==True:


    # ESTRATÈGIA BUY&HOLD
    # Si l'estratègia seleccionada és Buy&Hold, es calcula l'evolució de la inversió mantenint les accions fins al final
    if estratègia_inversió == "Buy&Hold":

        # Es calcula el nombre d'accions que es poden comprar amb el capital inicial
        accions_inicials= capital_inicial / dades_simulació["Open"].iloc[0]

        # Es creen dues llistes per emmagatzemar l'evolució del valor de la inversió i les dates corresponents
        valors_capital_buy_hold=[]
        dates_buy_hold=[]
        # https://www.geeksforgeeks.org/python/declare-an-empty-list-in-python/

        
        # Es recorren totes les dates disponibles de la taula de dades
        for dates_BH_act in dades_simulació.index: 
        # https://www.geeksforgeeks.org/pandas/iterating-over-rows-and-columns-in-pandas-dataframe/

            # S'obté el preu de tancament corresponent a cada data
             preu_tancament_dia=dades_simulació.loc[dates_BH_act,"Close"]
             # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.loc.html

            # Es calcula el valor de la inversió multiplicant el nombre d'accions pel preu de cada dia
             valor_inversió_dia = accions_inicials*preu_tancament_dia

            # S'afegeixen el valor calculat i la data corresponent a les seves llistes
             valors_capital_buy_hold.append(valor_inversió_dia)
             dates_buy_hold.append(dates_BH_act)
             # https://www.w3schools.com/python/ref_list_append.asp


        # Es crea un DataFrame amb l'evolució del capital i les dates corresponents
        dades_buy_hold = pd.DataFrame({
             "Capital":valors_capital_buy_hold,
             "Data": dates_buy_hold
        })
        # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.from_dict.html 
        
        
        # CÀLCULS DE BUY&HOLD 
        # Es calcula el valor final de la inversió a partir del nombre d'accions i del preu final
        valor_final_buy_hold= accions_inicials*dades_simulació["Close"].iloc[-1]

        # Es calcula el benefici obtingut respecte del capital inicial
        benefici_inversió= valor_final_buy_hold-capital_inicial 

         # Es calcula la rendibilitat de la inversió durant el període seleccionat
        rendibilitat_estratègia= (dades_simulació["Close"].iloc[-1]-dades_simulació["Open"].iloc[0])/dades_simulació["Open"].iloc[0]*100

        # Es calcula el màxim acumulat de la inversió per poder determinar el drawdown
        màxims_acumulats=pd.Series(valors_capital_buy_hold).cummax()# cummax no fiunciona a llistes, ha de ser un pandas 
        # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.cummax.html

        # Es calcula el drawdown de cada moment respecte del màxim acumulat
        drawdown=((pd.Series(valors_capital_buy_hold)/(màxims_acumulats))-1)*100
        
        # S'obté la caiguda màxima de la inversió a partir del valor més baix del drawdown
        drawdown_màxim=drawdown.min()
        # https://www.w3schools.com/python/ref_func_min.asp 

        # Es calculen els rendiments diaris de la inversió
        # El primer valor s'elimina perquè no disposa d'un valor anterior amb què comparar
        rendiments_diàris = pd.Series(valors_capital_buy_hold).pct_change().dropna()
        # https://www.geeksforgeeks.org/python/creating-a-pandas-series-from-lists/
        # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pct_change.html
        # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.dropna.html
        
        # S'estableix una taxa sense risc igual a zero per al càlcul del Sharpe
        taxa_sense_risc = 0

        # Es calcula el ràtio de Sharpe a partir del rendiment mitjà i la desviació estàndard
        ràtio_sharpe = (rendiments_diàris.mean() - taxa_sense_risc) / rendiments_diàris.std() * (252 ** 0.5)
        # https://pandas.pydata.org/docs/reference/api/pandas.Series.mean.html 
        # https://pandas.pydata.org/docs/reference/api/pandas.Series.std.html
        # https://www.investopedia.com/terms/s/sharperatio.asp
        
        # Es calcula la volatilitat anualitzada dels rendiments
        volatilitat_anualitzada = rendiments_diàris.std() * (252 ** 0.5) * 100


        # RESULTATS DE LA SIMULACIÓ BUY&HOLD
        # Es crea una línia horitzontal per separar els apartats de la simulació
        st.divider()
        # https://docs.streamlit.io/develop/api-reference/text/st.divider 

        # Es mostra el títol corresponent a la segona etapa
        st.subheader("Etapa 2")
        st.subheader("Evolució del capital amb BUY&HOLD")

        # GRÀFIC DE L'EVOLUCIÓ DEL CAPITAL
        # Es crea un gràfic de línies que representa l'evolució del capital al llarg del temps
        st.altair_chart(alt.Chart(dades_buy_hold).mark_line().encode( #no cal que creis una variable per desrpés fer altair_chart, ho pots fer directament
             x="Data:T",
             y="Capital:Q"
        )
        # https://altair-viz.github.io/user_guide/marks/line.html
        # https://altair-viz.github.io/user_guide/marks/line.html
        # https://altair-viz.github.io/user_guide/encodings/index.html

        # Faig que l'altura del gràfic sigui major
        .properties(height=600)
        )
        # https://altair-viz.github.io/user_guide/configuration.html

        # Es mostra l'apartat amb els principals resultats de la simulació
        st.subheader("Detalls de la simulació")
        
        # Es creen diferents columnes per distribuir visualment els resultats
        col_resultats,col3,col4,col5 = st.columns([5,1,1,1])#
        
        # Es treballa dins de la columna destinada als resultats
        with col_resultats:

            # Es crea un contenidor amb una vora per agrupar els detalls de la simulació
            with st.container(border=True):
             
             # Es divideix l'espai dels resultats en dues columnes
             col1,col2=st.columns(2)

        # Primera columna de resultats
        with col1: 
                
                # Es mostra el nombre d'accions comprades arrodonit a dos decimals
                st.write(f"Nombre d'accions comprades: {accions_inicials:,.2f}")
                # https://www.w3schools.com/PYTHON/python_string_formatting.asp 

                # Es mostra la rendibilitat expressada en percentatge i amb dos decimals
                st.write(f"Rendibilitat:\n{rendibilitat_estratègia:,.2f} % ")

                # Es mostra el màxim drawdown de la inversió
                st.write(f"Màxim Drawdown: {drawdown_màxim:,.2f} %")

                # Es mostra la volatilitat calculada
                st.write(f"Volatilitat: {volatilitat_anualitzada:,.2f} %")

                # Es mostra el ràtio de Sharpe calculat
                st.write(f"Sharpe: {ràtio_sharpe:,.2f}")
                
        # Segona columna de resultats         
        with col2:

                # Es mostra el benefici obtingut
                st.metric(
                    label="Benefici",
                    value= f"{benefici_inversió:,.2f} USD") 
                # https://docs.streamlit.io/develop/api-reference/data/st.metric

                # Es mostra el valor final de la simulació
                st.metric(
                label="Valor final",
                value=f"{valor_final_buy_hold:,.2f} USD"
                )
              

        # Es mantenen les columnes restants com a espai de separació visual
        with col3:
                st.write(" ")
        with col4:
                st.write(" ")
        with col5:
                st.write(" ")


        # GUARDAR LA SIMULACIÓ BUY&HOLD
        # Es crea un botó per permetre guardar la simulació
        boto_guardar_simulació= st.button("Guardar simulacio")

        # Si es prem el botó, es comprova si la simulació ja havia estat guardada
        if boto_guardar_simulació ==True:
             
            # Es crea una variable que indica si la simulació ja està guardada
             simulació_repetida=False

            # Es recorren les simulacions guardades per comprovar si n'hi ha alguna d'idèntica
             for simulacions in st.session_state.simulacions_guardades:
                  
                  ## Es comprova si coincideixen l'estratègia, l'empresa, el capital i les dates
                  if (simulacions["Estratègia"]=="Buy&Hold" and simulacions["Empresa"]== empresa_seleccionada and simulacions["Capital inicial"]==capital_inicial and simulacions["Data inici"]==data_1 and simulacions["Data final"]==data_final):
                       simulació_repetida=True

            # Si ja existeix una simulació amb les mateixes característiques, es mostra un avís      
             if simulació_repetida==True:
                       st.warning("No es pot repetir la mateixa simulació")

            # Si no existeix cap simulació igual, es crea un diccionari amb els resultats
             else:
                simulació_buy_hold= {"Estratègia":"Buy&Hold","Empresa":empresa_seleccionada,"Capital inicial":capital_inicial,"Valor final":valor_final_buy_hold,
                           "Benefici":benefici_inversió,"Rendibilitat":rendibilitat_estratègia,"Màxim Drawdown":drawdown_màxim,"Volatilitat":volatilitat_anualitzada,"Sharpe":ràtio_sharpe,
                           "Evolució capital": valors_capital_buy_hold,"Evolució dates": dates_buy_hold,"Data inici":data_1,"Data final":data_final,}
                
                # S'afegeix el diccionari amb els resultats a la llista de simulacions guardades
                st.session_state.simulacions_guardades.append(simulació_buy_hold)

                # Es mostra un missatge de confirmació
                st.write("Simulació guardada")

                # Es reinicia l'aplicació per actualitzar la informació de les simulacions guardades
                st.rerun()
                # https://docs.streamlit.io/develop/api-reference/execution-flow/st.rerun
    



    # ESTRATÈGIA DOLLAR COST AVERAGING (DCA)
    # Es defineix la condició perquè s'executi el codi quan l'estratègia seleccionada sigui DC
    elif estratègia_inversió == "Dollar Cost Averaging(DCA)":

                # DCA MENSUAL
                # Es comprova si la freqüència seleccionada és mensual
                if freqüència_DCA =="Mensual":

                    # Es compta el nombre de mesos diferents presents en el període de simulació
                    nombre_aportacions_DCA = dades_simulació.index.to_period("M").nunique()

                    # Es calcula la quantitat de diners que s'inverteix cada mes dividint el capital inicial entre el nombre de mesos
                    aportació_mensual= capital_inicial/nombre_aportacions_DCA# quants diners en cada mes
                    
                    # Es crea una llista per emmagatzemar el valor de la inversió de cada dia
                    valor_DCA_mensual =[]

                    # Es crea una llista per emmagatzemar les dates de la simulació
                    dates_DCA_mensuals=[]

                    # Es crea una llista per emmagatzemar el capital invertit acumulat
                    capital_invertit_acumulat=[]

                    # Es defineix el mes de referència inicial
                    # El valor 0 permet detectar el primer mes disponible de la simulació
                    mes_referència=0 

                    # Es defineix una variable per acumular el nombre total d'accions comprades
                    accions_totals_comprades=0

                    # Es defineix una variable per acumular el capital invertit
                    capital_invertit=0

                    # Es recorren totes les dates disponibles a la taula de dades
                    for dates_DCA_m in dades_simulació.index:
                         
                         # S'obté el preu de tancament corresponent a cada dia
                         preu_tancament_dia=dades_simulació.loc[dates_DCA_m,"Close"]

                         # Es transforma l'any i el mes en un únic valor numèric per identificar cada mes
                         mes_actual = dates_DCA_m.year * 12 + dates_DCA_m.month

                         # Es comprova si s'ha produït un canvi de mes
                         if mes_actual != mes_referència:
                              
                              # S'actualitza el mes de referència
                              mes_referència=mes_actual

                              # S'obté el preu d'obertura del primer dia disponible del mes
                              preu_obertura_mes=dades_simulació.loc[dates_DCA_m,"Open"]

                              # Es calcula el nombre d'accions que es poden comprar amb l'aportació mensual
                              accions_comprades_mes=aportació_mensual/preu_obertura_mes

                              # S'acumulen les accions comprades durant la simulació
                              accions_totals_comprades=accions_totals_comprades+accions_comprades_mes

                              # S'acumula l'import de la nova aportació al capital total invertit
                              capital_invertit=capital_invertit+aportació_mensual


                         # Es calcula el valor de les accions acumulades utilitzant el preu de tancament del dia
                         valor_inversió_dia= accions_totals_comprades*preu_tancament_dia 

                         # S'afegeix el valor calculat a la llista de valors de la simulació
                         valor_DCA_mensual.append(valor_inversió_dia)

                         # S'afegeix la data corresponent a la llista de dates
                         dates_DCA_mensuals.append(dates_DCA_m)

                         # S'afegeix el capital invertit acumulat a la llista corresponent
                         capital_invertit_acumulat.append(capital_invertit)



                    # Es crea un DataFrame amb el valor de la inversió, les dates i el capital invertit
                    dades_DCA_mensual= pd.DataFrame({
                        "Capital":valor_DCA_mensual,
                        "Data":dates_DCA_mensuals,
                        "Capital invertit":capital_invertit_acumulat
                                        })

                    # CÀLCULS DE DCA MENSUAL
                    # Es calcula el valor final de la inversió multiplicant les accions totals pel preu de tancament de l'últim dia
                    valor_final_DCA_mensual=accions_totals_comprades*dades_simulació["Close"].iloc[-1]

                    # S'obté el capital total invertit durant la simulació
                    capital_total_invertit=capital_invertit_acumulat[-1]

                    # Es calcula el benefici restant el capital invertit al valor final
                    benefici_DCA_mensual= valor_final_DCA_mensual-capital_inicial

                    # Es calcula la rendibilitat de la inversió en percentatge
                    rendibilitat_DCA_mensual= (valor_final_DCA_mensual-capital_inicial)*100/capital_inicial

                    # Per calcular el Sharpe i la volatilitat és necessari obtenir els rendiments de la inversió.
                    # En el DCA, el capital invertit augmenta en els dies en què es realitzen aportacions.
                    # Per aquest motiu, aquestes aportacions s'han de tenir en compte en el càlcul dels rendiments.
                    # Es converteix la llista dels valors diaris en una Series de pandas
                    taula_de_DCA_mensual_valor_diari = pd.Series(valor_DCA_mensual)
                    # https://pandas.pydata.org/docs/reference/api/pandas.Series.html

                    # Es converteix la llista del capital invertit acumulat en una Series de pandas
                    capital_invertit_serie = pd.Series(capital_invertit_acumulat)

                    # Es crea una llista per emmagatzemar els rendiments diaris calculats
                    rendiments_diaris = []

                    # Es recorren les posicions de la taula començant per la segona,
                    # Ja que cada valor s'ha de comparar amb el valor del dia anterior
                    for i in range(1, len(taula_de_DCA_mensual_valor_diari)):

                        # Es calcula la quantitat de capital nou introduït entre el dia actual i el dia anterior
                        nova_aportació = capital_invertit_serie.iloc[i] - capital_invertit_serie.iloc[i - 1]

                        # Es comprova si s'ha produït una nova aportació de capital
                        if nova_aportació > 0:

                            # Es calcula el rendiment del dia tenint en compte el capital aportat
                            rendiment_diari =taula_de_DCA_mensual_valor_diari.iloc[i] / (taula_de_DCA_mensual_valor_diari.iloc[i - 1] + nova_aportació)  - 1

                        # Si no s'ha produït cap aportació, es calcula el rendiment
                        # Comparant directament el valor actual amb el valor anterior
                        else:

                            # Es calcula la variació percentual del valor de la inversió entre els dos dies
                            rendiment_diari = (taula_de_DCA_mensual_valor_diari.iloc[i] / taula_de_DCA_mensual_valor_diari.iloc[i - 1]) - 1 
                            

                        # S'afegeix el rendiment calculat a la llista de rendiments diaris
                        rendiments_diaris.append(rendiment_diari)

                    # Es converteix la llista de rendiments en una Series de pandas
                    rendiments_diaris = pd.Series(rendiments_diaris)

                    # S'estableix la taxa sense risc en 0 per al càlcul del Sharpe
                    taxa_sense_risc =0 

                    # Es calcula el Sharpe a partir de la mitjana i la desviació estàndard dels rendiments diaris.
                    # El factor 252 ** 0.5 permet anualitzar el resultat considerant 252 dies de negociació.
                    ràtio_sharpe = (rendiments_diaris.mean() - taxa_sense_risc) / rendiments_diaris.std() * (252 ** 0.5)

                    # Es calcula la volatilitat anualitzada a partir de la desviació estàndard dels rendiments diaris i dels 252 dies de negociació anuals
                    volatilitat_anualitzada = rendiments_diaris.std() * (252 ** 0.5) * 100

                    # Es calcula l'evolució acumulada dels rendiments sense tenir en compte les aportacions
                    valor_sense_aportacions=(1+rendiments_diaris).cumprod()

                    # Es determina el valor màxim acumulat assolit en cada moment de la simulació
                    màxims_acumulats=valor_sense_aportacions.cummax()

                    # Es calcula el drawdown comparant cada valor amb el màxim acumulat corresponent
                    drawdown=(valor_sense_aportacions/màxims_acumulats -1)*100

                    # S'obté la caiguda percentual més gran registrada durant la simulació
                    drawdown_màxim=drawdown.min()


                    # RESULTATS DE LA SIMULACIÓ DCA MENSUAL
                    # Es separen visualment les diferents etapes de la simulació
                    st.divider()

                    # Es mostra el títol corresponent a la segona etapa
                    st.subheader("Etapa 2")

                    # Es mostra el títol del gràfic de l'evolució del capital amb DCA mensual
                    st.subheader("Evolució del capital amb DCA - mensual")


                    # GRÀFIC DE L'EVOLUCIÓ DEL CAPITAL
                    # Es transforma la taula per poder representar el capital i el capital invertit
                    # Ja que calen dues línies diferents dins del mateix gràfic
                    st.altair_chart(alt.Chart(dades_DCA_mensual).transform_fold(
                    # https://blog.stackademic.com/3-altair-transformations-to-save-you-time-cf84521fc74c

                    # S'indiquen les columnes que es convertiran en una única columna de valors
                    fold= ["Capital","Capital invertit"]
                    ).mark_line().encode(

                         # S'utilitza la data com a eix horitzontal 
                         x="Data:T",

                         # S'utilitzen els valors de les dues columnes com a eix vertical
                         y="value:Q",

                         # S'utilitza la clau generada per diferenciar les dues línies
                         color="key:N"

                    # S'estableix l'altura del gràfic en 600 píxels
                    ).properties(height=600))

                    # Es mostra el subtítol corresponent als detalls de la simulació
                    st.subheader("Detalls de la simulació")

                    # Es crea una estructura de columnes per distribuir els resultats de la simulació
                    col_resultats,col3,col4,col5 = st.columns([5,1,1,1])

                    # S'indica que es traballa amb la columna de resultats
                    with col_resultats:
                        # Es crea un contenidor amb una vora per agrupar els resultats
                         with st.container(border=True):

                            # Es creen dues altres columnes
                            col1,col2=st.columns(2)

                    # S'indica que es traballa amb la primera columna 
                    with col1: 

                        # Es mostra la quantitat de diners invertida en cada aportació mensual
                        st.write(f"Quants diners hi entren al mes: {aportació_mensual:,.2f} USD")

                        # Es mostra el nombre total d'accions comprades durant la simulació
                        st.write(f"Nombre d'accions comprades: {accions_totals_comprades:,.2f} ")
                        
                        # Es mostra la rendibilitat obtinguda durant la simulació
                        st.write(f"Rendibilitat: {rendibilitat_DCA_mensual:,.2f} %")


                        # Es mostra el màxim Drawdown obtingut
                        st.write(f"Màxim Drawdown: {drawdown_màxim:,.2f} %")

                        # Es mostra la volatilitat anualitzada obtinguda
                        st.write(f"Volatilitat: {volatilitat_anualitzada:,.2f} %")
                    
                        # Represento el sharpe
                        st.write(f"Sharpe: {ràtio_sharpe:,.2f}")

                       
                    # S'indica que es traballa amb la segona columna 
                    with col2:

                        # Es mostra el benefici obtingut durant la simulació
                        st.metric(
                             label="Benefici del DCA:",
                             value= f"{benefici_DCA_mensual:,.2f} USD")
                        
                        # Es mostra el valor final de la inversió.
                        st.metric(
                            label="Valor final del DCA:",
                            value= f"{valor_final_DCA_mensual:,.2f} USD")


                    # GUARDAR LA SIMULACIÓ DCA MENSUAL
                    # Es crea un botó per permetre guardar la simulació
                    boto_guardar_simulació= st.button("Guardar simulacio")

                    # Es comprova si s'ha premut el botó de guardar la simulació
                    if boto_guardar_simulació ==True:

                        # Es defineix una variable per indicar si la simulació ja està guardada
                        simulació_repetida=False

                        # Es recorren totes les simulacions guardades anteriorment
                        for simulacions in st.session_state.simulacions_guardades:

                             # Es comprova si coincideixen l'estratègia, l'empresa, el capital inicial les dates i la freqüència amb la simulació actual
                             if (simulacions["Estratègia"]=="DCA mensual" and simulacions["Empresa"]== empresa_seleccionada and simulacions["Capital inicial"]==capital_inicial and simulacions["Data inici"]==data_1 and simulacions["Data final"]==data_final and simulacions.get("Frequència")==freqüència_DCA):
                                  simulació_repetida=True

                        # S'indica que ja existeix una simulació amb les mateixes característiques      
                        if simulació_repetida==True:

                            # Si la simulació ja existeix, es mostra un avís a l'usuari
                             st.warning("No es pot repetir la mateixa simulació")

                        # Si no existeix cap simulació igual, es crea i es guarda la nova simulació
                        else:
                            # Es crea un diccionari amb les dades principals de la simulació DCA mensual
                            simulació_DCA_mensual= {"Estratègia":"DCA mensual","Empresa":empresa_seleccionada,"Capital inicial":capital_inicial,"Valor final":valor_final_DCA_mensual,"Benefici":benefici_DCA_mensual,"Rendibilitat":rendibilitat_DCA_mensual,"Màxim Drawdown":drawdown_màxim,"Volatilitat":volatilitat_anualitzada,"Sharpe":ràtio_sharpe,
                                        "Evolució capital":valor_DCA_mensual,"Evolució dates": dates_DCA_mensuals,"Data inici":data_1,"Data final":data_final,"Frequència":freqüència_DCA}
                            
                            # S'afegeix el diccionari a la llista de simulacions guardades
                            st.session_state.simulacions_guardades.append(simulació_DCA_mensual)

                            # Es mostra un missatge indicant que la simulació s'ha guardat correctament
                            st.write("Simulació guardada")  

                            # Es reinicia l'aplicació per actualitzar l'estat de les simulacions guardades
                            st.rerun()                  

                    

                # DCA ANUAL
                # Es comprova si la freqüència seleccionada és anual
                elif freqüència_DCA =="Anual":

                     # Es compta el nombre d'anys diferents presents en el període de simulació
                     nombre_anys=dades_simulació.index.year.nunique() 
                     # https://pandas.pydata.org/docs/reference/api/pandas.DatetimeIndex.year.html
                     # https://pandas.pydata.org/docs/reference/api/pandas.Series.nunique.html

                     # Es calcula la quantitat de diners que s'inverteix cada any dividint el capital inicial entre el nombre d'anys
                     aportació_anual= capital_inicial/nombre_anys

                     # Es crea una llista per emmagatzemar el valor de la inversió de cada dia
                     valor_final_DCA_anual=[]

                     # Es crea una llista per emmagatzemar les dates de la simulació
                     dates_DCA_anuals=[]

                     # Es crea una llista per emmagatzemar el capital invertit acumulat
                     capital_invertit_acumulat=[]

                     # Es defineix l'any de referència inicial
                     any_referència=0
                     
                     # Es defineix una variable per acumular el nombre total d'accions comprades
                     accions_totals_comprades=0

                     # Es defineix una variable per acumular el capital invertit
                     capital_invertit=0

                     # Es recorren totes les dates disponibles a la taula de dades
                     for dates_DCA_a in dades_simulació.index:
                          # S'obté el preu de tancament corresponent a cada dia
                          preu_tancament_dia=dades_simulació.loc[dates_DCA_a,"Close"]

                          # S'obté l'any corresponent a la data actual
                          any_actual= dates_DCA_a.year

                          # Es comprova si s'ha produït un canvi d'any
                          if any_actual!=any_referència:

                                # S'actualitza l'any de referència amb l'any actual
                                any_referència=any_actual

                                # S'obté el preu d'obertura del primer dia disponible de l'any
                                preu_obertura_any=dades_simulació.loc[dates_DCA_a,"Open"]

                                # Es calcula el nombre d'accions que es poden comprar amb l'aportació anual
                                accions_comprades_any= aportació_anual/preu_obertura_any

                                # S'acumulen les accions comprades durant la simulació
                                accions_totals_comprades=accions_totals_comprades+accions_comprades_any

                                # S'acumula l'import de la nova aportació al capital total invertit
                                capital_invertit=capital_invertit+aportació_anual

                          # Es calcula el valor de les accions acumulades utilitzant el preu de tancament del dia
                          valor_inversió_dia=accions_totals_comprades*preu_tancament_dia

                          # S'afegeix el valor calculat a la llista de valors de la simulació
                          valor_final_DCA_anual.append(valor_inversió_dia)

                          # S'afegeix la data corresponent a la llista de dates
                          dates_DCA_anuals.append(dates_DCA_a)

                          # S'afegeix el capital invertit acumulat a la llista corresponent
                          capital_invertit_acumulat.append(capital_invertit)

                     # Es crea un DataFrame amb el valor de la inversió, les dates i el capital invertit
                     dades_DCA_anual=pd.DataFrame({
                         "Capital":valor_final_DCA_anual,
                         "Data":dates_DCA_anuals,
                         "Capital invertit":capital_invertit_acumulat
                     })


                     # CÀLCULS DE DCA ANUAL
                     # Es calcula el valor final de la inversió multiplicant les accions totals pel preu de tancament de l'últim dia
                     valor_final_DCA_a= accions_totals_comprades*dades_simulació["Close"].iloc[-1]

                     # S'obté el capital total invertit durant la simulació             
                     total_invertit_a=capital_invertit_acumulat[-1]

                     # Es calcula el benefici restant el capital invertit al valor final de la inversió
                     benefici_DCA_anual= valor_final_DCA_a-capital_inicial

                     # Es calcula la rendibilitat de la inversió en percentatge
                     rendibilitat_DCA_anual= (valor_final_DCA_a-capital_inicial)*100/capital_inicial

                     # Per calcular el Sharpe i la volatilitat és necessari obtenir els rendiments de la inversió.
                     # En el DCA, el capital invertit augmenta en els dies en què es realitzen aportacions.
                     # Per aquest motiu, aquestes aportacions s'han de tenir en compte en el càlcul dels rendiments.

                     # Es converteix la llista dels valors diaris en una Series de pandas
                     taula_de_DCA_anual_valor_diari = pd.Series(valor_final_DCA_anual)
 
                     # Es converteix la llista del capital invertit acumulat en una Series de pandas
                     capital_invertit_serie = pd.Series(capital_invertit_acumulat)

                     # Es crea una llista per emmagatzemar els rendiments diaris calculats
                     rendiments_diaris = []

                     # Es recorren les posicions de la taula començant per la segona, ja que cada valor s'ha de comparar amb el valor del dia anterior
                     for i in range(1, len(taula_de_DCA_anual_valor_diari)):

                        # Es calcula la quantitat de capital nou introduït entre el dia actual i el dia anterior
                        nova_aportació = capital_invertit_serie.iloc[i] - capital_invertit_serie.iloc[i - 1]

                        # Es comprova si s'ha produït una nova aportació de capital
                        if nova_aportació > 0:

                            # Es calcula el rendiment del dia tenint en compte el capital aportat
                            rendiment_diari = (taula_de_DCA_anual_valor_diari.iloc[i] /(taula_de_DCA_anual_valor_diari.iloc[i - 1] + nova_aportació)) - 1

                        # Si no s'ha produït cap aportació, es calcula el rendiment comparant directament el valor actual amb el valor anterior 
                        else:

                            # Es calcula la variació percentual del valor de la inversió entre els dos dies
                            rendiment_diari = (taula_de_DCA_anual_valor_diari.iloc[i] / taula_de_DCA_anual_valor_diari.iloc[i - 1]) - 1

                        # S'afegeix el rendiment calculat a la llista de rendiments diaris
                        rendiments_diaris.append(rendiment_diari)

                     # Es converteix la llista de rendiments en una Series de pandas
                     rendiments_diàris = pd.Series(rendiments_diaris)

                     # S'estableix la taxa sense risc en 0 per al càlcul del Sharpe
                     taxa_sense_risc = 0

                     # Es calcula el Sharpe a partir de la mitjana i la desviació estàndard dels rendiments diaris
                     # El factor 252 ** 0.5 permet anualitzar el resultat considerant 252 dies de negociació
                     ràtio_sharpe = (rendiments_diàris.mean() - taxa_sense_risc) / rendiments_diàris.std() * (252 ** 0.5)

                     # Es calcula la volatilitat anualitzada a partir de la desviació estàndard dels rendiments diaris
                     volatilitat_anualitzada = rendiments_diàris.std() * (252 ** 0.5) * 100

                     # Es calcula l'evolució acumulada dels rendiments sense tenir en compte les aportacions
                     valor_sense_aportacions=(1+rendiments_diàris).cumprod()

                     # Es determina el valor màxim acumulat assolit en cada moment de la simulació
                     màxims_acumulats=valor_sense_aportacions.cummax()

                     # Es calcula el drawdown comparant cada valor amb el màxim acumulat corresponent
                     drawdown=(valor_sense_aportacions/màxims_acumulats -1)*100

                     # S'obté la caiguda percentual més gran registrada durant la simulació
                     drawdown_màxim=drawdown.min()
                     

                    # RESULTATS DE LA SIMULACIÓ DCA ANUAL
                    # Es separen visualment les diferents etapes de la simulació
                     st.divider()

                     # Es mostra el títol corresponent a la segona etapa
                     st.subheader("Etapa 2")

                     # Es mostra el títol del gràfic de l'evolució del capital amb DCA anual
                     st.subheader("Evolució del capital amb DCA - anual")

                     # GRÀFIC DE L'EVOLUCIÓ DEL CAPITAL
                     # Es transforma la taula per poder representar el capital i el capital invertit
                     st.altair_chart(alt.Chart(dades_DCA_anual).transform_fold(fold=["Capital","Capital invertit"]).mark_line().encode(
                           
                          # S'utilitza la data com a eix horitzontal 
                          x="Data:T",

                          # S'utilitzen els valors de les dues columnes com a eix vertical
                          y="value:Q",

                          # S'utilitza la clau generada per diferenciar les dues línies
                          color="key:N"

                     # S'estableix l'altura del gràfic en 600 píxels
                     ).properties(height=600))

                     # Es mostra el subtítol corresponent als detalls de la simulació
                     st.subheader("Detalls de la simulació")

                    # Es crea una estructura de columnes per distribuir els resultats de la simulació
                     col_resultats,col3,col4,col5 = st.columns([5,1,1,1])

                     # S'indica que es treballarà amb la columna de resultats
                     with col_resultats:
                            
                            # Es crea un contenidor amb una vora per agrupar els resultats
                            with st.container(border=True):

                                # Es divideix el contenidor principal en dues columnes
                                col1,col2=st.columns(2)

                     # S'indica que es treballarà amb la primera columna
                     with col1: 
                            
                            # Es mostra la quantitat de diners invertida en cada aportació anual
                            st.write(f"Quants diners hi entren a l'any : {aportació_anual:,.2f} USD")

                            # Es mostra el nombre total d'accions comprades durant la simulació
                            st.write(f"Nombre d'accions comprades: {accions_totals_comprades:,.2f}")


                            # Es mostra la rendibilitat obtinguda durant la simulació
                            st.write(f"Rendibilitat : {rendibilitat_DCA_anual:,.2f} %")

                            # Es mostra el màxim Drawdown obtingut                                   
                            st.write(f"Màxim Drawdown: {drawdown_màxim:,.2f} %")

                            # Es mostra la volatilitat anualitzada obtinguda
                            st.write(f"Volatilitat: {volatilitat_anualitzada:,.2f} %")

                            # Es mostra el valor del Sharpe obtingut
                            st.write(f"Sharpe: {ràtio_sharpe:,.2f}")
                   

                     # S'indica que es treballa amb la segona columna
                     with col2:
                            
                            # Es mostra el benefici obtingut durant la simulació
                            st.metric(
                                label="Benefici del DCA:",
                                value= f"{benefici_DCA_anual:,.2f} USD")

                            # Es mostra el valor final de la inversió
                            st.metric(
                                label="Valor final del DCA:",
                                value= f"{valor_final_DCA_a:,.2f} USD")
                     

                     # GUARDAR LA SIMULACIÓ DCA ANUAL
                     # Es crea un botó per permetre guardar la simulació
                     boto_guardar_simulació= st.button("Guardar simulacio")

                     # Es comprova si s'ha premut el botó de guardar la simulació
                     if boto_guardar_simulació ==True:

                        # Es defineix una variable per indicar si la simulació ja està guardada
                        simulació_repetida=False

                        # Es recorren totes les simulacions guardades anteriorment
                        for simulacions in st.session_state.simulacions_guardades:

                                # # Es comprova si coincideixen l'estratègia, l'empresa, el capital inicial, les dates i la freqüència amb la simulació actual
                                if (simulacions["Estratègia"]=="DCA anual" and simulacions["Empresa"]== empresa_seleccionada and simulacions["Capital inicial"]==capital_inicial and simulacions["Data inici"]==data_1 and simulacions["Data final"]==data_final and simulacions.get("Frequència")==freqüència_DCA):
                                   
                                    # S'indica que ja existeix una simulació amb les mateixes característiques 
                                    simulació_repetida=True

                        # Si la simulació ja existeix, es mostra un avís
                        if simulació_repetida==True:
                            st.warning("No es pot repetir la mateixa simulació")

                        # Si no existeix cap simulació igual, es crea i es guarda la nova simulació
                        else:

                            # Es crea un diccionari amb les dades principals de la simulació DCA anual
                            simulació_DCA_anual= {"Estratègia":"DCA anual","Empresa":empresa_seleccionada,"Capital inicial":capital_inicial,"Valor final":valor_final_DCA_a,"Benefici":benefici_DCA_anual,"Rendibilitat":rendibilitat_DCA_anual,"Màxim Drawdown":drawdown_màxim,"Volatilitat":volatilitat_anualitzada,"Sharpe":ràtio_sharpe,
                                        "Evolució capital": valor_final_DCA_anual,"Evolució dates": dates_DCA_anuals,"Data inici":data_1,"Data final":data_final,"Frequència":freqüència_DCA}

                            # S'afegeix el diccionari a la llista de simulacions guardades
                            st.session_state.simulacions_guardades.append(simulació_DCA_anual)

                            # Es mostra un missatge indicant que la simulació s'ha guardat correctament
                            st.write("Simulació guardada")

                            # Es reinicia l'aplicació per actualitzar l'estat de les simulacions guardades
                            st.rerun()


    # ESTRATÈGIA STOP-LOSS I TAKE-PROFIT      
    # Es comprova si l'estratègia seleccionada és Stop-Loss i Take-Profit
    elif estratègia_inversió == "Stop-Loss i Take-Profit":

        # Es calcula el nombre d'accions que es poden comprar amb el capital inicial
        accions_inicials= capital_inicial/dades_simulació["Open"].iloc[0]

        # Es mostra el subtítol corresponent a la selecció dels percentatges
        st.subheader("Tria els percentatges")

        # Es defineix una funció per reiniciar l'estat de la simulació quan es modifiquen els percentatges
        def canvi_percentatges():
         st.session_state.Simulació_començada=False

        # TRIA DE PARÀMETRES
        # Es crea un slider per seleccionar el percentatge de pèrdua màxima del capital inicial
        # Aquest percentatge determina el nivell en què s'activarà el Stop-Loss
        percentatge_stop_loss = st.slider(
        label="Stop-Loss",
        min_value= 1,
        max_value=100,
        value=20,
        step =1,
        # Si es modifica el percentatge, s'executa la funció canvi_percentatges
        on_change=canvi_percentatges
        )

        # Es calcula el preu de l'acció corresponent al nivell del Stop-Loss
        preu_Stop_Loss= dades_simulació["Open"].iloc[0]-(dades_simulació["Open"].iloc[0]*percentatge_stop_loss/100)

        # Es calcula el valor del capital corresponent al nivell del Stop-Loss
        capital_stop_loss=preu_Stop_Loss*accions_inicials

        # Es mostra el valor del capital corresponent al nivell del Stop-Loss
        st.markdown(f"###### Valor: {capital_stop_loss:,.2f} USD")


        # Es crea un slider per seleccionar el percentatge de guany del capital inicial
        # Aquest percentatge determina el nivell en què s'activarà el Take-Profit
        percentatge_take_profit= st.slider(
        label="Take-Profit",
        min_value=1,
        max_value=300,
        value=50,
        step=1,
        on_change=canvi_percentatges
                )

        # Es calcula el preu de l'acció corresponent al nivell del Take-Profit
        preu_Take_Profit = dades_simulació["Open"].iloc[0]+(dades_simulació["Open"].iloc[0]*percentatge_take_profit/100)

        # Es calcula el valor del capital corresponent al nivell del Take-Profit
        capital_take_profit= preu_Take_Profit*accions_inicials

        # Es mostra el valor del capital corresponent al nivell del Take-Profit
        st.markdown(f"###### Valor:{capital_take_profit:,.2f} USD")


        # Es mostra el valor del capital corresponent al nivell del Take-Profit
        if "Simulació_començada" not in st.session_state: #La variable ya existe, así que no vuelve a crearla. La cajita sigue teniendo: TRUE

         # Es defineix l'estat inicial de la variable com a False
         st.session_state.Simulació_començada = False

        # Es crea el botó per iniciar la simulació
        boto_començar= st.button(
        label="Començar simulació"
        )

        # Es comprova si s'ha premut el botó d'inici de la simulació
        # En aquest cas, l'estat de la simulació passa a ser True
        if boto_començar== True:
         st.session_state.Simulació_començada = True

        # Es comprova si la simulació està activa
        if st.session_state.Simulació_començada == True:

        # Es creen dues llistes buides per emmagatzemar els valors del capital i les dates
            capital_stop_take_profit=[]
            dates_stop_take_profit=[]

            # Es calcula el nombre d'accions comprades amb el capital inicial
            accions_inicials= capital_inicial/dades_simulació["Open"].iloc[0]


            # Es recorren totes les dates disponibles a la taula de dades
            for dates_ST_act in dades_simulació.index:
                        
                        # S'obté el preu de tancament corresponent al dia actual
                        preu_tancament_dia=dades_simulació.loc[dates_ST_act,"Close"]

                        # S'obté el preu mínim assolit durant el dia
                        # Aquest valor permet comprovar si s'ha assolit el nivell de Stop-Loss
                        preu_mínim=dades_simulació.loc[dates_ST_act,"Low"]

                        # S'obté el preu màxim assolit durant el dia
                        # Aquest valor permet comprovar si s'ha assolit el nivell de Take-Profit
                        preu_màxim=dades_simulació.loc[dates_ST_act,"High"]

    
                        # Es comprova si el preu màxim del dia ha assolit o superat el nivell de Take-Profit
                        if preu_màxim >= preu_Take_Profit: # ejemplo si tope es 130 i tk es 120 estonces que se activ  proque para ellgar al 130 tien que pasar por el 120

                             # Es fixa el preu de la simulació en el nivell del Take-Profit
                             preu_dia_stop_take_profit=preu_Take_Profit

                             # S'indica que la simulació s'ha aturat pel Take-Profit
                             motiu_parada_simulació="take"

                            
                             # Es calcula l'últim valor del capital en el moment de l'aturada
                             capital_dia_stop_take_profit=accions_inicials*preu_Take_Profit

                             # S'afegeix el valor del capital a la llista corresponent
                             capital_stop_take_profit.append(capital_dia_stop_take_profit)

                             # S'afegeix la data de l'aturada a la llista corresponent
                             dates_stop_take_profit.append(dates_ST_act)

                             # Es finalitza el recorregut perquè la simulació s'ha aturat
                             break

                        # Si no s'ha assolit el Take-Profit, es comprova si s'ha assolit el Stop-Loss
                        elif preu_mínim <= preu_Stop_Loss:
                        
                                                    # Es fixa el preu de la simulació en el nivell del Stop-Loss
                                                    preu_dia_stop_take_profit=preu_Stop_Loss
                        
                                                    # S'indica que la simulació s'ha aturat pel Stop-Loss
                                                    motiu_parada_simulació="stop"
                                                    
                                                   # Es calcula l'últim valor del capital en el moment de l'aturada
                                                    capital_dia_stop_take_profit=accions_inicials*preu_Stop_Loss
                        
                                                    # S'afegeix el valor del capital a la llista corresponent
                                                    capital_stop_take_profit.append(capital_dia_stop_take_profit)
                        
                                                   # S'afegeix la data de l'aturada a la llista corresponent
                                                    dates_stop_take_profit.append(dates_ST_act)
                        
                        
                                                    # Es finalitza el recorregut perquè la simulació s'ha aturat
                                                    break
                                                    # https://www.geeksforgeeks.org/python/python-break-statement/
                        

                        # Si no s'assoleix cap dels dos nivells, la simulació continua fins al dia següent
                        else:

                             # Es fixa el preu del dia en el preu de tancament corresponent
                             preu_dia_stop_take_profit=preu_tancament_dia
  
                             # S'indica que la simulació no s'ha aturat per cap dels dos nivells
                             motiu_parada_simulació="no_top"

                             # Es calcula el valor del capital corresponent al dia actual
                             capital_dia_stop_take_profit=accions_inicials*preu_dia_stop_take_profit

                             # S'afegeix el valor calculat a la llista de capitals
                             capital_stop_take_profit.append(capital_dia_stop_take_profit)

                             # S'afegeix la data corresponent a la llista de dates
                             dates_stop_take_profit.append(dates_ST_act)




            # Es crea una taula amb els valors del capital i les dates acumulades durant la simulació
            dades_stop_take_profit=pd.DataFrame({
                        "Capital":capital_stop_take_profit,
                        "Data":dates_stop_take_profit
                    })

            # CÀLCULS DE STOP-LOSS I TAKE-PROFIT
            # Es calcula el valor final de la inversió a partir del preu final i del nombre d'accions
            valor_final_stop_take_profit =  preu_dia_stop_take_profit*accions_inicials

            # Es calcula el benefici restant el capital inicial al valor final
            benefici_inversió= valor_final_stop_take_profit-capital_inicial

            # Es calcula la rendibilitat de la inversió en percentatge
            rendibilitat_estratègia= (capital_stop_take_profit[-1]-capital_inicial)/capital_inicial*100

            # Es converteix la llista de valors del capital en una Series de pandas i s'obtè el màxim acumulat de la sèria
            màxims_acumulats=pd.Series(capital_stop_take_profit).cummax()

            # Es calcula el drawdown comparant cada valor amb el màxim acumulat corresponent
            drawdown=((pd.Series(capital_stop_take_profit)/(màxims_acumulats))-1)*100

            # S'obté la caiguda percentual més gran registrada durant la simulació
            drawdown_màxim=drawdown.min()

            # Es calcula el canvi percentual entre els valors consecutius de la  i s'elimina el primer valor
            rendiments_diàris = pd.Series(capital_stop_take_profit).pct_change().dropna()

            # S'estableix la taxa sense risc en 0 per al càlcul del Sharpe
            taxa_sense_risc = 0

            # Es calcula el Sharpe a partir de la mitjana i la desviació estàndard dels rendiment
            ràtio_sharpe = (rendiments_diàris.mean() - taxa_sense_risc) / rendiments_diàris.std() * (252 ** 0.5)

            # Es calcula la volatilitat anualitzada a partir de la desviació estàndard dels rendiments
            volatilitat_anualitzada = rendiments_diàris.std() * (252 ** 0.5) * 100

            # RESULTATS DE LA SIMULACIÓ STOP-LOSS I TAKE-PROFIT
            # Es mostra el subtítol corresponent als detalls de la simulació
            st.subheader("Detalls de la simulació")

            # Es separen visualment les diferents parts de la informació
            st.divider()

            # Es mostra el títol corresponent a la segona etapa
            st.subheader("Etapa 2")

            # Es mostra el títol del gràfic de l'evolució del capital
            st.subheader("Evolució del capital ST")

            # GRÀFIC DE STOP-LOSS I TAKE-PROFIT
            # Es crea el gràfic de l'evolució del capital a partir de la taula de dades
            st.altair_chart(alt.Chart(dades_stop_take_profit).mark_line().encode(
                  
                # S'utilitza la data com a eix horitzontal
                x="Data:T",

                # S'utilitza el capital com a eix vertical
                y="Capital:Q"

            # Es fixa l'altura del gràfic en 600 píxels
            ).properties(height=600))

            # Es crea una estructura de columnes per distribuir els resultats de la simulació
            col_resultats,col3,col4,col5 = st.columns([5,1,1,1])

            # S'indica que es treballa en la columna dels resultats
            with col_resultats:
                 
                # Es crea un contenidor amb una vora per agrupar els detalls de la simulació
                with st.container(border=True):

                    # El contenidor principal es divideix en dues columnes
                    col1,col2=st.columns(2)

            # S'indica que es treballa en la primera columna 
            with col1: 

                # Es mostra el motiu pel qual s'ha aturat la simulació
                st.write("Motiu:")           

                # Es comprova si la simulació s'ha aturat pel Stop-Loss  
                if motiu_parada_simulació== "stop":              
                    st.write("S'ha parat gràcies al Stop-Loss")

                # Es comprova si la simulació s'ha aturat pel Stop-Loss
                elif motiu_parada_simulació== "take":
                    st.write("S'ha parat gràcies al Take-Profit")

                # Es comprova si la simulació no s'ha aturat per cap dels dos nivells
                elif motiu_parada_simulació=="no_top":
                    st.write("La simulació no ha arribat a cap màxim i mínim")

                # Es mostra el nombre total d'accions comprades, arrodonit a dos decimals           
                st.write(f"Nombre d'accions comprades: {accions_inicials:,.2f} ") 

                # Es mostra la rendibilitat obtinguda durant la simulació
                st.write(f"Rendibilitat : {rendibilitat_estratègia:,.2f} %") 

                # Es mostra el màxim Drawdown obtingut                     
                st.write(f"Màxim Drawdown: {drawdown_màxim:,.2f} %")

                # Es mostra la volatilitat anualitzada obtinguda
                st.write(f"Volatilitat: {volatilitat_anualitzada:,.2f} %")

                # Es mostra el valor del Sharpe obtingut
                st.write(f"Sharpe: {ràtio_sharpe:,.2f}")

            # S'indica que es treballa amb la segona columna
            with col2: 

                # Es mostra el benefici obtingut amb una mida destacada
                st.metric(
                    label="Benefici:",
                    value= f"{benefici_inversió:,.2f} USD")
                
                # Es mostra el valor final de la simulació amb una mida destacada
                st.metric(
                    label="Valor finals:",
                    value= f"{valor_final_stop_take_profit:,.2f} USD")
                                
            

            # GUARDAR LA SIMULACIÓ STOP-LOSS I TAKE-PROFIT
            # Es crea un botó per permetre guardar la simulació
            boto_guardar_simulació= st.button("Guardar simulacio")

            # Es comprova si s'ha premut el botó de guardar la simulació
            if boto_guardar_simulació ==True:

                # Es defineix una variable per indicar si la simulació ja està guardada
                simulació_repetida=False

                # Es recorren totes les simulacions guardades anteriorment
                # Si la llista està buida, no es realitza cap comprovació
                for simulacions in st.session_state.simulacions_guardades:
                        
                        # Es comprova si coincideixen l'estratègia, l'empresa, el capital inicial, les dates i els percentatges de Stop-Loss i Take-Profit
                        if (simulacions["Estratègia"]=="Stop-Loss i Take-Profit" and simulacions["Empresa"]== empresa_seleccionada and simulacions["Capital inicial"]==capital_inicial and simulacions["Data inici"]==data_1 and simulacions["Data final"]==data_final and simulacions["Stop-Loss"]==percentatge_stop_loss and simulacions["Take-Profit"]==percentatge_take_profit):
                            # Es detecta que hi ha una simulació repetida
                            simulació_repetida=True


                # Si ja existeix una simulació amb les mateixes característiques, es mostra un avís    
                if simulació_repetida==True:
                        st.warning("No es pot repetir la mateixa simulació")

                # Si no existeix cap simulació igual, es crea i es guarda la nova simulació   
                else:

                    # Es crea un diccionari amb les dades principals de la simulació Stop-Loss i Take-Profit
                    simulació_stop_take_profit= {"Estratègia":"Stop-L i Take-P","Empresa":empresa_seleccionada,"Capital inicial":capital_inicial,"Valor final":valor_final_stop_take_profit,"Benefici":benefici_inversió,"Rendibilitat":rendibilitat_estratègia,"Màxim Drawdown":drawdown_màxim,"Volatilitat":volatilitat_anualitzada,"Sharpe":ràtio_sharpe,"Stop-Loss":percentatge_stop_loss,"Take-Profit":percentatge_take_profit,
                            "Evolució capital":capital_stop_take_profit,"Evolució dates":dates_stop_take_profit,"Data inici":data_1,"Data final":data_final}

                    # S'afegeix el diccionari a la llista de simulacions guardades
                    st.session_state.simulacions_guardades.append(simulació_stop_take_profit)

                    # Es mostra un missatge indicant que la simulació s'ha guardat correctament
                    st.write("Simulació guardada")

                    # Es reinicia l'aplicació per actualitzar l'estat de les simulacions guardades             
                    st.rerun()


            # STIO-LOSS I TAKE-PROFIT SENSE LÍMITS
            # Es creen dues llistes per emmagatzemar l'evolució del capital en el cas que no s'apliquin els límits       
            capital_ST_max = []
            dates_ST_max =[]

            # Es recorren totes les dates disponibles per calcular l'evolució del capital sense límits
            for dates_ST_capital_max in dades_simulació.index:

                            # S'obté el preu de tancament corresponent al dia actual
                            preu_dia_stop_take_profit=dades_simulació.loc[dates_ST_capital_max,"Close"]

                            # Es calcula el valor del capital corresponent al dia actual
                            capital_dia_ST_max=accions_inicials*preu_dia_stop_take_profit

                            # S'afegeix el valor calculat a la llista de capitals                                   
                            capital_ST_max.append(capital_dia_ST_max)

                            # S'afegeix la data corresponent a la llista de dates
                            dates_ST_max.append(dates_ST_capital_max)


            # Es crea una taula amb l'evolució del capital i les dates sense aplicar cap límit   
            taula_max = pd.DataFrame({ #aqui cal data frame i es parèntesis
                    "Capital":capital_ST_max,
                    "Dates":dates_ST_max
                })


            # CÀLCULS DE STOP-LOSS I TAKE-PROFIT SENSE LÍMITS
            # Es calcula el valor final de la simulació sense aplicar cap límit
            valor_final_ST_max = accions_inicials *dades_simulació["Close"].iloc[-1]

            # Es calcula el benefici restant el capital inicial al valor final sense límits
            benefici_max= valor_final_ST_max-capital_inicial

            # Es calcula la rendibilitat de la simulació sense límits
            rendibilitat_max= (capital_ST_max[-1]-capital_inicial)/capital_inicial*100


            # RESULTATS DE LA SIMULACIÓ STOP-LOSS I TAKE-PROFIT SENSE LÍMITS
            # Es crea un botó perquè l'usuari pugui consultar l'evolució de la inversió sense aplicar els límits
            Capital_max=st.button(
                    label= "Si no hagués límits"  
                )

           # Es comprova si s'ha premut el botó per mostrar l'evolució sense límits
            if Capital_max==True:


                    # GRÀFIC DE STOP-LOSS I TAKE-PROFIT SENSE LÍMITS    
                    # Es crea el gràfic de l'evolució completa del capital sense límits
                    st.altair_chart(alt.Chart(taula_max).mark_line().encode(
                          
                        # S'utilitza la data com a eix horitzontal
                        x="Dates:T",

                        # S'utilitza el capital com a eix vertical
                        y="Capital:Q"

                    # Es fixa l'altura del gràfic en 600 píxels
                    ).properties(height=600))

                    # Es crea una estructura de columnes per distribuir els resultats
                    col_resultats,col3,col4,col5 = st.columns([3,1,1,1])

                    # S'indica que es treballa en la columna dels resultats
                    with col_resultats:

                        # Es crea un contenidor amb una vora per agrupar els resultats
                        with st.container(border=True):

                                # Es creen dues altres columnes
                                col1,col2=st.columns(2)

                    # S'indica que es treballa en la primera columna 
                    with col1: 

                        # Es representa la rendibilitat
                        st.write(f"Rendibilitat: {rendibilitat_max:,.2f} %")

                        
                    # S'indica que es treballa en la segona columna                        
                    with col2:

                        # Es mostra el benefici amb una mida destacada
                        st.metric(
                            label="Benefici",
                            value= f"{benefici_max:,.2f} USD") 

                        # Es mostra el valor final de la simulació amb una mida destacada
                        st.metric(
                        label="Valor final",
                        value=f"{valor_final_ST_max:,.2f} USD"
                        )
                

    # ESTRATÈGIA DIVERSIFICACIÓ
    # Es comprova si l'estratègia seleccionada és Diversificació
    elif estratègia_inversió == "Diversificació":

        # TRIA DE PARÀMETRES
        # Es separa visualment aquesta secció de l'anterior
        st.divider()

        # Es mostra l'opció per seleccionar el nombre d'empreses
        st.write("**Tria el número d'empreses per diversificar:**")

        # Es creen dues columnes per situar el selector en la posició desitjada
        colum1,espacio = st.columns([0.35,3])
        with colum1:
         
        # Es crea un selector per determinar el nombre d'empreses de la cartera
         nombre_empreses=st.number_input(
                label=" ",
                min_value= 2,
                max_value=10,
                value=2,
                step=1,
                label_visibility="collapsed"# buscar video
            
        )

        # Es crea un diccionari que associa cada sector amb les empreses corresponents
        empreses={"Tecnologia":["Apple","Microsoft","Nvidia","TSMC","Adobe"],
                "Financer":["JPMorgan Chase","Goldman Sachs","American Express","Visa","Mastercard"],
                "Serveis digitals":["Amazon","eBay","Booking Holdings","Cisco Systems","Alphabet"],
                "Energia":["ExxonMobil","Chevron","NextEra Energy","AES","EQT"],
                "Salut":["UnitedHealth Group","McKesson","CVS Health","Amgen","Pfizer"],
                "Inmobiliari":["D.R. Horton","Lennar","Hovnanian Enterprises","PulteGroup","Toll Brothers"],
                "Automoció":["Volkswagen","Toyota   ","PACCAR","Ford","Honda"],
                "Consum":["Walmart","Nestlé","Coca-Cola","PepsiCo","Procter&Gamble"]}#Creem això per a que ens deixi posar les mepreses i el sector al for, busacsr video

        # Es crea una llista per emmagatzemar les empreses seleccionades
        empreses_seleccionades=[]

        # Es crea una llista per emmagatzemar els percentatges assignats a cada empresa
        percentatges_seleccionats =[]

        # Es crea una llista per emmagatzemar el capital destinat a cada empresa
        distribució_capital=[]

        # Es defineix una funció per reiniciar l'estat del botó d'inici quan es modifica la configuració
        def canvi_sector_empresa_percentatge():
         st.session_state.boto_començar=False

    
        # Es recorren totes les empreses seleccionades per l'usuari
        for i in range(nombre_empreses):

            # Es crea un contenidor amb una vora per agrupar les opcions de cada empresa  
            with st.container(border=True):

                # Es creen tres columnes diferents
                col1,col2,col3=st.columns(3)

                # S'indica que es treballa en la primera columna
                with col1:

                     # Es mostra el selector del sector corresponent a cada empresa
                    sector_seleccionar=st.selectbox(
                            label=f"Tria el sector de l'empresa {i+1}",
                            options =["Tecnologia","Financer","Serveis digitals","Energia","Salut","Inmobiliari","Automoció","Consum"],

                            # Es defineix una clau única per diferenciar cada selector
                            key=f"sector_{i}",
                            on_change= canvi_sector_empresa_percentatge
                    )

                # S'indica que es treballa en la segona columna   
                with col2:
                    empresa_seleccionar= st.selectbox(
                            label=f"Tria l'empresa {i+1}",

                            # Es mostren únicament les empreses que pertanyen al sector seleccionat
                            options=empreses[sector_seleccionar],

                            # Es defineix una clau única per diferenciar cada selector
                            key=f"empresa_{i}",
                            on_change= canvi_sector_empresa_percentatge
                    )

               # S'indica que es treballa en la tercera columna   
                with col3:

                    # Es mostra el selector del percentatge de capital destinat a l'empresa
                    percentatges_seleccionat=st.slider(
                            label=f"Tria el percentatge de l'empresa {i+1}",
                            min_value=1,
                            max_value=99,
                            value=50,
                            step=1,
                            # Es defineix una clau única per diferenciar cada slider
                            key=f"percentatge{i}",
                            on_change=canvi_sector_empresa_percentatge
                    )

                    # Es calcula la quantitat de capital destinada a l'empresa seleccionada
                    mostrar_percentatge= capital_inicial*percentatges_seleccionat/100

                    # Es mostra el capital destinat a l'empresa
                    st.write(f"Capital inicial: {mostrar_percentatge:.0f} USD")

                    # S'afegeix el capital destinat a l'empresa a la llista corresponent
                    distribució_capital.append(mostrar_percentatge)

                
            # S'afegeix l'empresa seleccionada a la llista d'empreses
            empreses_seleccionades.append(empresa_seleccionar)

            # S'afegeix el percentatge seleccionat a la llista corresponent
            percentatges_seleccionats.append(percentatges_seleccionat)

        # Es comprova si hi ha empreses repetides en la selecció
        if len(empreses_seleccionades) != len(set(empreses_seleccionades)):
        # https://www.youtube.com/shorts/U2DcHWloBFQ
                st.write("No pot haver empreses repetides")

        # Es comprova que els percentatges sumin exactament 100% i que no hi hagi empreses repetides  
        elif sum(percentatges_seleccionats)== 100 and len(empreses_seleccionades)== len(set(empreses_seleccionades)):
        
            # Es crea una llista per emmagatzemar les dades obtingudes de cada empresa   
            guardar_dades = []

            # Es defineix una variable per indicar si s'ha produït algun error amb les dates o les dades
            error_dates = False

            # OBTENCIÓ DE LES DADES HISTÒRIQUES
            # Es recorren totes les empreses seleccionades per obtenir les seves dades  
            for empresa_dades in empreses_seleccionades:

                    # S'obté el ticker corresponent a l'empresa seleccionada
                    ticker = diccionari_tickers[empresa_dades]

                    # Es crea l'objecte de yfinance corresponent al ticker
                    ticker_empresa = yh.Ticker(ticker)

                    # S'obté l'historial de dades de l'empresa dins del període seleccionat
                    dades_empresa = ticker_empresa.history(start=data_inici_diversificació,end=data_final_diversificació,auto_adjust=True)
            
                    # Es comprova si s'han obtingut dades per al període seleccionat
                    if dades_empresa.empty:
                        st.warning(f"No hi ha dades per a {empresa_dades} en aquest període.")

                        # Es modifica la variable d'error per indicar que no es poden obtenir les dades
                        error_dates = True

                        # Es finalitza el recorregut de les empreses
                        break

                    # S'afegeixen les dades de l'empresa a la llista corresponent
                    guardar_dades.append(dades_empresa)

 
            # Es comprova que no s'hagi produït cap error durant l'obtenció de dades
            if not error_dates:

                # S'obtenen inicialment les dates disponibles de la primera empresa
                    dates_comunes_empreses = guardar_dades[0].index

                   # Es recorren les dades de les empreses restants
                    for dades in guardar_dades[1:]:
                        # https://www.askpython.com/python/list/x-in-a1-mean-python

                        # Es sincronitzen el totes les dades de cada empresa
                        dates_comunes_empreses = dates_comunes_empreses.intersection(dades.index)
                        # https://www.w3schools.com/python/ref_set_intersection.asp


                    # Es comprova si existeix almenys una data comuna entre totes les empreses
                    if len(dates_comunes_empreses) == 0:
                        st.warning("Les empreses no tenen dates de cotització en comú.")

                    # Si existeixen dates comunes, es continua amb la simulació
                    else:

                    # Es conserven únicament les dades de cada empresa corresponents a les dates comunes
                        guardar_dades = [dades.loc[dates_comunes_empreses]
                                         
                        for dades in guardar_dades
                        # https://elpythonista.com/list-comprehensions-python
                        ]




                        # Es combinen les empreses, el capital destinat i les seves dades mitjançant zip
                        dades_accions_empreses= zip(empreses_seleccionades,distribució_capital,guardar_dades)
                        # https://www.geeksforgeeks.org/python/zip-in-python/ 


                        # Es crea una llista per emmagatzemar els valors de totes les empreses
                        empreses_seleccionades=[]

                        # Es crea una llista per emmagatzemar els noms de les empreses       
                        noms_empreses=[]
                    
                        # Es crea una llista per emmagatzemar el valor final de cada empresa
                        valor_final_empresa =[]

                        # Es crea un diccionari per associar cada empresa amb la seva evolució de capital
                        dades_gràfic_empreses_individual={} 

                       
                        # Es recorren les dades corresponents a cada empresa, al capital destinat i al seu període           
                        for empresa,diners_distribució,dades_simulació in dades_accions_empreses:  

                                # S'obté el preu d'obertura del primer dia de la simulació
                                preu_obertura= dades_simulació["Open"].iloc[0]

                                # Es calcula el nombre d'accions que es poden comprar amb el capital destina
                                accions_comprades= diners_distribució/preu_obertura


                                # S'obté el preu de tancament de l'últim dia de la simulació
                                preu_tancament = dades_simulació["Close"].iloc[-1]

                                # Es calcula el valor final de cada empresa
                                valor_final= preu_tancament*accions_comprades

                                # S'afegeix el valor final de l'empresa a la llista corresponent
                                valor_final_empresa.append(valor_final)
                                
                                # S'afegeix el nom de l'empresa a la llista corresponent
                                noms_empreses.append(empresa)

                                # Es crea una llista per emmagatzemar els valors diaris de cada empresa
                                valors_de_cada_empresa=[]

                                                                    
                                # Es recorren totes les dates disponibles de l'empresa
                                for dates_DIS_act in dades_simulació.index:
                                        
                                        # S'obté el preu de tancament corresponent a cada dia
                                        preu_tancament_dia=dades_simulació.loc[dates_DIS_act,"Close"]

                                        # Es calcula el valor de les accions de l'empresa en cada dia
                                        valor_inversió_dia=accions_comprades*preu_tancament_dia #las acciones no canvian, canvia su precio. EX:10 acciones, precio dia 2: 1100, 10 *110$, dia 3: 900, 10*90$

                                        # S'afegeix el valor diari a la llista corresponent
                                        valors_de_cada_empresa.append(valor_inversió_dia) # valors_de_cada_empresa ↓ [6000, 6050, 5900, 6100]


                                # S'afegeixen els valors de l'empresa a la llista que conté totes les empreses   
                                empreses_seleccionades.append(valors_de_cada_empresa) 

                                # S'associa cada empresa amb la seva evolució de capital dins del diccionari
                                dades_gràfic_empreses_individual[empresa]=valors_de_cada_empresa # aqui ponemos empresa porque asi cada vuelta detecta en que empresa esta en esa vuelta, si pusiera "APPLE" estaria mal
                                

                        # Es crea un DataFrame amb l'evolució individual de cada empresa
                        taula_de_cada_empresa_individual=pd.DataFrame( # No cal un diccionari perque ja tinc els nombs de les columnes
                        dades_gràfic_empreses_individual)

                        # Es crea una columna amb les dates comunes corresponents als valors de cada empresa
                        taula_de_cada_empresa_individual["Dates"]= dates_comunes_empreses 
                                


                        # Ara que ja es disposa de tots els valors de cada empresa
                        # S'han de sumar per a crear un únic gràfic amb tots els valors
                        #Primer creo la llista
                        capital_total_invertit=[]

                        # Es recorren totes les posicions temporals de les dades 
                        for i in range(len(empreses_seleccionades[0])):#range no pot ser una lista
                        # https://docs.python.org/es/3.7/tutorial/introduction.html

                                            # Es defineix el capital del dia actual inicialment com a 0
                                            capital_invertit_dia=0

                                            # Es recorren les dades de totes les empreses per sumar-ne el valor
                                            for empresa in empreses_seleccionades:

                                                # S'afegeix el valor de cada empresa corresponent al dia actual
                                                capital_invertit_dia= capital_invertit_dia+ empresa[i] # [2000, 2000, 2200], valor de esta empresa en este dia

                                            # S'afegeix el capital total del dia a la llista corresponent   
                                            capital_total_invertit.append(capital_invertit_dia)# tiene que estar fuera porque queremos guardar una solo suma por dia, no una suma por cada empresa
                                
                                    
                        # Es crea un DataFrame amb l'evolució del capital total i les dates 
                        dades_diversificació = pd.DataFrame({
                                            "Capital":capital_total_invertit,
                                            "Data":dates_comunes_empreses
                                    })

                        # CÀLCULS DE DIVERSIFICACIÓ
                        # Es calcula el valor final de la cartera
                        valor_final= capital_total_invertit[-1]

                        # Es calcula el benefici restant el capital inicial al valor final
                        benefici_inversió= valor_final-capital_inicial

                        # Es calcula la rendibilitat de la inversió en percentatge
                        rendibilitat= (valor_final-capital_inicial)/capital_inicial*100

                        # Es calcula el màxim acumulat del capital total
                        màxims_acumulats=pd.Series(capital_total_invertit).cummax()

                        # Es calcula el Drawdown comparant cada valor amb el màxim acumulat corresponent
                        drawdown=((pd.Series(capital_total_invertit)/(màxims_acumulats))-1)*100

                        # S'obté la caiguda percentual més gran registrada durant la simulació   
                        drawdown_màxim=drawdown.min()

                        # Es calcula el canvi percentual entre els valors consecutius del capital total
                        rendiments_diàris = pd.Series(capital_total_invertit).pct_change().dropna()

                        # S'estableix la taxa sense risc en 0 per al càlcul del Sharpe                                               
                        taxa_sense_risc = 0

                        # Es calcula el Sharpe a partir de la mitjana i la desviació estàndard dels rendiments   
                        ràtio_sharpe = (rendiments_diàris.mean() - taxa_sense_risc) / rendiments_diàris.std() * (252 ** 0.5)

                        # Es calcula la volatilitat anualitzada a partir de la desviació estàndard dels rendiments
                        volatilitat_anualitzada = rendiments_diàris.std() * (252 ** 0.5) * 100            

                        # RESULTATS DE LA SIMULACIÓ STOP-LOSS I TAKE-PROFIT
                        # Es crea el botó per iniciar la simulació
                        boto_començar= st.button(
                            label="Començar simulació",

                            # Es defineix una clau única per identificar el botó dins de Streamlit
                            key="boto_diversificació"
                    )

                        # Es comprova si s'ha premut el botó d'inici de la simulació
                        if boto_començar==True:
                            st.session_state.boto_començar=True

                        # Es comprova si la simulació està activa
                        if st.session_state.boto_començar== True:

                                        # Es separen visualment les diferents etapes de la simulació
                                        st.divider()

                                        # Es mostra el títol corresponent a la segona etapa
                                        st.subheader("Etapa 2")

                                        # Es mostra el títol del gràfic de l'evolució del capital total
                                        st.subheader("Gràfic total")

                                        # GRÀFIC DEL CAPITAL DE DIVERSIFICACIÓ
                                        # Es crea el gràfic amb l'evolució del capital total de la cartera
                                        st.altair_chart(alt.Chart(dades_diversificació).mark_line().encode(

                                            # S'utilitza la data com a eix horitzontal  
                                            x="Data:T",

                                            # S'utilitza el capital total com a eix vertical
                                            y="Capital:Q"
                                        ).properties(height=600))

                                        
                                        
                                        # Es mostra el subtítol corresponent als detalls de la inversió
                                        st.subheader("Detalls de la inversió")

                                        # Es crea una estructura de columnes per distribuir els resultats
                                        # Les columnes addicionals s'utilitzen com a espai de separació
                                        col_resultats,col3,col4,col5 = st.columns([5,1,1,1])

                                        # Es crea un contenidor amb una vora per agrupar els resultats
                                        # El contenidor principal es divideix en dues columnes
                                        with col_resultats:
                                            with st.container(border=True):

                                                # Es creen dos columnes noves
                                                col1,col2=st.columns(2)

                                        # S'indica que es treballa amb la primera columna
                                        with col1: 

                                            # Es mostra la rendibilitat obtinguda durant la simulació
                                            st.write(f"Rendibilitat : {rendibilitat:,.2f} %") 

                                            # Es mostra el màxim Drawdown obtingut
                                            st.write(f"Màxim Drawdown: {drawdown_màxim:,.2f} %")

                                            # Es mostra la volatilitat anualitzada obtinguda
                                            st.write(f"Volatilitat: {volatilitat_anualitzada:,.2f} %")

                                            # Es mostra el valor del Sharpe obtingut
                                            st.write(f"Sharpe: {ràtio_sharpe:,.2f}")

                                        
                                        # S'indica que es treballa amb la segona columna   
                                        with col2:   

                                            # Es mostra el benefici obtingut amb una mida destacada
                                            st.metric(
                                                label="Benefici:",
                                                value= f"{benefici_inversió:,.2f} USD")

                                            # Es mostra el valor final de la simulació amb una mida destacada
                                            st.metric(
                                                label="Valor final:",
                                                value=f"{valor_final:,.2f} USD"
                                            )
                                        
                                        # Es mostra el títol del gràfic individual de cada empresa
                                        st.subheader("Gràfic de cada empresa")

                                        # GRÀFIC INDIVIDUALS DE DIVERSIFICACIÓ
                                        # Es transforma la taula per representar l'evolució de totes les empreses en un únic gràfic
                                        st.altair_chart(alt.Chart(taula_de_cada_empresa_individual).transform_fold(noms_empreses).mark_line().encode(

                                            # S'utilitzen les dates com a eix horitzontal
                                            x="Dates:T",

                                            # S'utilitzen els valors de cada empresa com a eix vertical
                                            y="value:Q",

                                            # S'utilitza el nom de l'empresa per diferenciar les diferents línies
                                            color="key:N"

                                        ).properties(height=600))

                                        # Es mostra el títol corresponent als detalls de cada empresa
                                        st.subheader("Detalls de la simulació:")

                                        # Es creen dues columnes per distribuir la informació
                                        col1,espai=st.columns([1.6,3])

                                        # S'indica que es treballa amb la primera columna
                                        with col1:

                                            # S'estableix el contorn
                                            with st.container(border=True):

                                                    # Es mostra el títol dels valors finals
                                                    st.markdown("##### Valor final")

                                                    # Es recorren totes les empreses per mostrar el seu valor final
                                                    for i in range(len(noms_empreses)):

                                                            # Es mostra el valor final corresponent a cada empresa
                                                            st.metric(
                                                                label=f"{noms_empreses[i]} USD",
                                                                value= f"{valor_final_empresa[i]:,.2f} USD")


                                        # GUARDAR LA SIMULACIÓ DIVERSIFICACIÓ
                                        # Es crea un botó per permetre guardar la simulació
                                        boto_guardar_simulació= st.button("Guardar simulacio")

                                        # Es comprova si s'ha premut el botó de guardar la simulació
                                        if boto_guardar_simulació ==True:

                                            # Es defineix una variable per indicar si la simulació ja està guardada
                                            simulació_repetida=False

                                            # Es recorren totes les simulacions guardades anteriorment
                                            for simulacions in st.session_state.simulacions_guardades:

                                                # Es comprova si coincideixen l'estratègia, les empreses, el capital inicial i les dates
                                                if (simulacions["Estratègia"]=="Diversificació" and simulacions["Empresa"]== ",".join(noms_empreses) and simulacions["Capital inicial"]==capital_inicial and simulacions["Data inici"]==data_inici_diversificació and simulacions["Data final"]==data_final_diversificació):
                                                    
                                                    # I directament es detecta que hi ha una simulació repetida
                                                    simulació_repetida=True

                                            # Si ja existeix una simulació amb les mateixes característiques, es mostra un avís 
                                            if simulació_repetida==True:
                                                st.warning("No es pot repetir la mateixa simulació")

                                            # Si no existeix cap simulació igual, es crea i es guarda la nova simulació    
                                            else:

                                                # Es crea un diccionari amb les dades principals de la simulació de diversificació
                                                simulació_diversificació= {"Estratègia":"Diversificació","Empresa":",".join(noms_empreses),#join lo que hace es que el nombre de las emrpesas me las junta en solo un mismo texto TypeError: can only concatenate list (not "str") to list
                                                        "Capital inicial":capital_inicial,"Valor final":valor_final,"Benefici":benefici_inversió,"Rendibilitat":rendibilitat,"Màxim Drawdown":drawdown_màxim,"Volatilitat":volatilitat_anualitzada,"Sharpe":ràtio_sharpe, "Evolució capital":  capital_total_invertit,"Evolució dates": dates_comunes_empreses,"Data inici":data_inici_diversificació,"Data final":data_final_diversificació}

                                                # S'afegeix el diccionari a la llista de simulacions guardades
                                                st.session_state.simulacions_guardades.append(simulació_diversificació)

                                                # Es mostra un missatge indicant que la simulació s'ha guardat correctament
                                                st.write("Simulació guardada")

                                                # Es reinicia l'aplicació per actualitzar l'estat de les simulacions guardades
                                                st.rerun()



        # Es comprova si la suma dels percentatges supera el 100%           
        elif sum(percentatges_seleccionats) > 100:
            st.write("La suma dels percentatges no pot superar el 100%")
            st.write("Intenta-ho modificar")

        # Es comprova si la suma dels percentatges és inferior al 100%
        elif sum(percentatges_seleccionats) < 100: 
            st.write("La suma dels percentatges ha de ser igual a 100%")
            st.write("Intenta-ho modificar") 