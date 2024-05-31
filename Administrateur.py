import pandas as pd
import pymysql.cursors
import streamlit as st
from st_pages import Page, show_pages
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_pages import Page, show_pages, hide_pages

# Identification des onglets à faire apparaître
show_pages([
    Page("Variation_forte.py","Accueil"),
    Page("Administrateur.py","Admin"),
    Page("pages/testKarim.py","PU REC"),
    Page("pages/testKarimpareto.py","Analyse CC"),
    Page("pages/testKarimCodeOpeUnique.py","Contrôle Code Opérateur"),
    Page("pages/testAllouCodeOpeUnique.py","Contrôle Code Opérateur 2"),
    Page("pages/testAllou.py","Recherche"),
    Page("pages/Controle_All.py","Croisement"),
    Page("pages/testAlloupareto.py","Analyse Valeurs"),
    Page("pages/testAllouEspeces.py","Analyse Espèces"),
    Page("pages/ControleNiveau1.py","Contrôle 1er niveau"),
    Page("pages/Controle.py","Controle"),
    Page("pages/Controle_CIAB1.py","Controle1"),
    Page("pages/Controle_CIAB3.py","Controle3"),
    Page("pages/Controle_CIAB5.py","Controle5"),
    Page("pages/Controle_CIAB6.py","Controle6"),
    Page("pages/Controle_CIAB7.py","Controle7"),
    Page("pages/Controle_CIABP.py","ControleP"),
    Page("pages/BazRec.py","RecherceBaz"),
    Page("pages/BazAnalyse.py","AnalyseBaz"),
    Page("pages/Controle_RFCV.py","ContrôleRFCV"),
    Page("pages/Suivi_CodeOperateurRFCV.py","Suivi Opérateur RFCV"),
    Page("pages/ControleNiveau1RFCV.py","Contrôle 1er niveau RFCV"),
    Page("pages/ControleNiveau1RFCVKarim.py","Contrôle 1er niveau RFCV Karim")
])

hide_pages(['Contrôle 1er niveau', 'Controle', 'Controle1', 
            'Controle3', 'Controle5', 'Controle6', 'Controle7', 'ControleP',
             'Recherche', 'Croisement', 'Analyse Valeurs', 'PU REC', "Contrôle Code Opérateur",
             "Analyse Espèces", "Analyse CC", "Contrôle Code Opérateur 2", "RecherceBaz", "AnalyseBaz",
             'ContrôleRFCV', 'Suivi Opérateur RFCV', 'Contrôle 1er niveau RFCV',
             "Contrôle 1er niveau RFCV Karim"
             ])  

#show_pages([
    #Page("Variation_forte.py","Accueil"),
    #Page("Administrateur.py","Admin")
#])



#Etablir la connexion
#@st.cache_resource
def init_connection():
    host        = 'sql11.freemysqlhosting.net' # 'sql205.infinityfree.com' #
    user        = 'sql11664568' # 'if0_36410890' #
    password    = 'fMJHRX62M7' #'ZiZROzlMya'#
    database    = 'sql11664568' # 'if0_36410890_douanesci'#
    cursorclass = pymysql.cursors.DictCursor
    return pymysql.connect(host=host, database=database, user=user, password=password, cursorclass=cursorclass)

mydb = init_connection()

mycursor = mydb.cursor()


def main():
    st.title("Opérations de l'administrateur d'utilisateurs")

    # Display Options for CRUD Operations
    option=st.sidebar.selectbox("Sélectionner une opération",("Créer","Lire","Modifier"))
    # Perform Selected CRUD Operations
    if option=="Créer":
        st.subheader("Créer un nouvel utilisateur")
        mycursor.execute("select * from bureau")
        resultBur = pd.DataFrame(mycursor.fetchall())

        mycursor.execute("select * from basededonnees")
        resultBDD = pd.DataFrame(mycursor.fetchall())

        mycursor.execute("select * from habilitation")
        resultACC = pd.DataFrame(mycursor.fetchall())

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
            mycursor.execute(sql,val)
            mydb.commit()
            st.success("Enregistrement réussi!!!")
            


    elif option=="Lire":
        st.subheader("Les utilisateurs dans la base")
        mycursor.execute("select * from utilisateur")
        result = mycursor.fetchall()
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
                    mycursor.execute(sql,val)
                    mydb.commit()
                    st.success("Suppression réussie!!!")


    elif option=="Modifier":
        st.subheader("Modifiier un enregistrement")
        id=st.number_input("Enter ID",min_value=1)

        mycursor.execute("select * from utilisateur")
        result = mycursor.fetchall()
        result = pd.DataFrame(result)
        result = result[result.ID==id]


        if result.shape[0]==1:
            with st.form(key= 'modifier', clear_on_submit=True):
                nom=st.text_input("nouveau Nom", result['Nom'].iloc[0])
                prenom=st.text_input("nouveau Prénom", result['Prenom'].iloc[0])
                bur=st.text_input("nouveau Bureau", result['Bureau'].iloc[0])
                bdd=st.text_input("Base de données", result['BDD'].iloc[0])
                acc=st.text_input("Privilège d'accès", result['Acces'].iloc[0])
                identifiant=st.text_input("nouvel identifiant de connexion", result['Identifiant'].iloc[0])
                password=st.text_input("nouveau mot de passe", result['Password'].iloc[0])
                modifier_button = st.form_submit_button('Modifier')
                
            if modifier_button:
                sql="update utilisateur set nom=%s, prenom=%s, bureau=%s, bdd=%s, acces=%s, identifiant=%s, password=%s where id =%s"
                val= (nom,prenom,bur,bdd,acc,identifiant,password,id)
                mycursor.execute(sql,val)
                mydb.commit()
                st.success("Mise à jour réussie!!!")
        else:
            st.write("Cet identifiant n'est pas créé.")

if mycursor:
    if __name__ == "__main__":
        main()
else:
    st.write("Connexion impossible à établir")
