import os
import pandas as pd
import pymysql
import streamlit as st
from st_pages import Page, show_pages
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_pages import Page, show_pages, hide_pages

#***********************************************************************
show_pages([
    Page("Variation_forte.py","Accueil"),
    Page("Administrateur.py","Admin")
])

hide_pages([
    Page("pages/Controle_RFCV.py","ContrôleRFCV"),
    Page("pages/Suivi_CodeOperateurRFCV.py","Suivi Opérateur RFCV"),
    Page("pages/testEspecesRFCV.py","Frêt")
])



timeout=int(os.getenv('timeout')) or st.secrets["timeout"]

connection = pymysql.connect(
    connect_timeout=timeout,
    cursorclass=pymysql.cursors.DictCursor,
    db=os.getenv('db') or st.secrets["db"],
    host= os.getenv('host') or st.secrets["host"],
    password= os.getenv('password') or st.secrets["password"],
    read_timeout=timeout,
    port=int(os.getenv("port") if os.getenv("port").isdigit() else os.getenv("port")[4:-1]) or st.secrets["port"],
    user= os.getenv('user') or st.secrets["user"],
    write_timeout=timeout
)

try:
    cursor = connection.cursor()
    
except:
    st.write('pas ok') 
    
    
def main():
    st.title("Opérations de l'administrateur d'utilisateurs")

    # Display Options for CRUD Operations
    option=st.sidebar.selectbox("Sélectionner une opération",("Créer","Lire","Modifier"))
    # Perform Selected CRUD Operations
    if option=="Créer":
        st.subheader("Créer un nouvel utilisateur")
        cursor.execute("select * from bureau")
        resultBur = pd.DataFrame(cursor.fetchall())

        cursor.execute("select * from basededonnees")
        resultBDD = pd.DataFrame(cursor.fetchall())

        cursor.execute("select * from habilitation")
        resultACC = pd.DataFrame(cursor.fetchall())

        nom=st.text_input("Nom",'')
        prenom=st.text_input("Prénom")
        bur=st.selectbox("Bureau", [' '] + list(resultBur['NomBureau']))
        bdd=st.selectbox("Base de données", [' '] + list(resultBDD['BDD']))
        if bdd == 'Décisionnel':
            acc=st.selectbox("Privilège d'accès", [' '] + ['Manager', 'Vérificateur'])
        if bdd == 'BAZREC':
            acc=st.selectbox("Privilège d'accès", [' '] + ['Manager', 'Vérificateur'])
        if bdd == 'RFCV':
            acc=st.selectbox("Privilège d'accès", [' '] + ['CB', 'CV', 'Vérificateur'])
        identifiant=st.text_input("Identifiant de connexion")
        password=st.text_input("Mot de passe")
        
        if st.button("Créer"):
            sql= "insert into utilisateur(nom,prenom,bureau,bdd,acces,identifiant,password) values(%s,%s,%s,%s,%s,%s,%s)"
            val= (nom,prenom,bur,bdd,acc,identifiant,password)
            cursor.execute(sql,val)
            connection.commit()
            st.success("Enregistrement réussi!!!")
            


    elif option=="Lire":
        st.subheader("Les utilisateurs dans la base")
        cursor.execute("select * from utilisateur")
        result = cursor.fetchall()
        result = pd.DataFrame(result)

        gd = GridOptionsBuilder.from_dataframe(result)
        gd.configure_pagination(enabled=True)
        gd.configure_default_column(editable=True, groupable=True)
        gd.configure_selection(selection_mode="multiple", use_checkbox=True)
        gridoptions = gd.build()
        grid_table = AgGrid(
            result,
            gridOptions=gridoptions,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            theme="material",
        )

        df_sel_row = pd.DataFrame(grid_table["selected_rows"])

        if df_sel_row.shape[0] > 0:
            if st.button("Supprimer"):
                for id in df_sel_row['ID']:
                    sql="delete from utilisateur where id =%s"
                    val=(id,)
                    cursor.execute(sql,val)
                    connection.commit()
                    st.success("Suppression réussie!!!")

    elif option=="Modifier":
        st.subheader("Modifier un enregistrement")
        #id=st.number_input("Entrer ID",min_value=1)

        cursor.execute("select * from utilisateur")
        result = cursor.fetchall()
        result = pd.DataFrame(result)
        #result['ID'] = result['ID'].astype(int)
        id=st.selectbox("Entrer ID", result['ID'].unique())
        result = result[result.ID==id]


        if result.shape[0]==1:
            with st.form(key= 'modifier', clear_on_submit=True):
                nom=st.text_input("nouveau Nom", result['nom'].iloc[0])
                prenom=st.text_input("nouveau Prénom", result['prenom'].iloc[0])
                bur=st.text_input("nouveau Bureau", result['bureau'].iloc[0])
                bdd=st.text_input("Base de données", result['bdd'].iloc[0])
                acc=st.text_input("Privilège d'accès", result['acces'].iloc[0])
                identifiant=st.text_input("nouvel identifiant de connexion", result['identifiant'].iloc[0])
                password=st.text_input("nouveau mot de passe", result['password'].iloc[0])
                modifier_button = st.form_submit_button('Modifier')
                
            if modifier_button:
                sql="update utilisateur set nom=%s, prenom=%s, bureau=%s, bdd=%s, acces=%s, identifiant=%s, password=%s where id =%s"
                val= (nom,prenom,bur,bdd,acc,identifiant,password,id)
                cursor.execute(sql,val)
                connection.commit()
                st.success("Mise à jour réussie!!!")
        else:
            st.write("Cet identifiant n'est pas créé.")

if cursor:
    if __name__ == "__main__":
        main()
else:
    st.write("Connexion impossible à établir")