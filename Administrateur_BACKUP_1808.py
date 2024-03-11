import pandas as pd
<<<<<<< HEAD
import mysql.connector  # version  mysql.connector-2.2.9
import streamlit as st
from st_pages import Page, show_pages
=======
import pymysql.cursors
import streamlit as st
from st_pages import Page, show_pages
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder
>>>>>>> master

show_pages([
    Page("Variation_forte.py","Accueil"),
    Page("Administrateur.py","Admin")
])


#Etablir la connexion
<<<<<<< HEAD
mydb = mysql.connector.connect(
    host = 'sql11.freemysqlhosting.net',
    user = 'sql11664568',
    password = 'fMJHRX62M7',
    database = 'sql11664568'
)
=======
#@st.cache_resource
def init_connection():
    host        = 'sql11.freemysqlhosting.net'
    user        = 'sql11664568'
    password    = 'fMJHRX62M7'
    database    = 'sql11664568'
    cursorclass = pymysql.cursors.DictCursor
    return pymysql.connect(host=host, database=database, user=user, password=password, cursorclass=cursorclass)

mydb = init_connection()
>>>>>>> master

mycursor = mydb.cursor()


def main():
    st.title("Opérations de l'administrateur d'utilisateurs")

    # Display Options for CRUD Operations
<<<<<<< HEAD
    option=st.sidebar.selectbox("Sélectionner une opération",("Créer","Lire","Modifier","Supprimer"))
    # Perform Selected CRUD Operations
    if option=="Créer":
        st.subheader("Créer un nouvel utilisateur")

=======
    option=st.sidebar.selectbox("Sélectionner une opération",("Créer","Lire","Modifier"))
    # Perform Selected CRUD Operations
    if option=="Créer":
        st.subheader("Créer un nouvel utilisateur")
>>>>>>> master
        mycursor.execute("select * from bureau")
        resultBur = pd.DataFrame(mycursor.fetchall())

        mycursor.execute("select * from basededonnees")
        resultBDD = pd.DataFrame(mycursor.fetchall())

        mycursor.execute("select * from habilitation")
        resultACC = pd.DataFrame(mycursor.fetchall())

        nom=st.text_input("Nom",'')
        prenom=st.text_input("Prénom")
<<<<<<< HEAD
        bur=st.selectbox("Bureau", list(resultBur.loc[:,1]))
        identifiant=st.text_input("Identifiant de connexion")
        password=st.text_input("Mot de passe")
        bdd=st.selectbox("Base de données", list(resultBDD.loc[:,1]))
        if bdd == 'Decisionnel':
            acc=st.selectbox("Privilège d'accès", ['Manager', 'Vérificateur'])
        if bdd == 'RFCV':
            acc=st.selectbox("Privilège d'accès", ['CB', 'CV'])
        if st.button("Créer"):
            sql= "insert into utilisateur(nom,prenom,bureau,identifiant,password,bdd,acces) values(%s,%s,%s,%s,%s,%s,%s)"
            val= (nom,prenom,bur,identifiant,password,bdd,acc)
=======
        bur=st.selectbox("Bureau", [' '] + list(resultBur['NomBureau']))
        bdd=st.selectbox("Base de données", [' '] + list(resultBDD['BDD']))
        if bdd == 'Décisionnel':
            acc=st.selectbox("Privilège d'accès", [' '] + ['Manager', 'Vérificateur'],)
        if bdd == 'RFCV':
            acc=st.selectbox("Privilège d'accès", [' '] + ['CB', 'CV'])
        identifiant=st.text_input("Identifiant de connexion")
        password=st.text_input("Mot de passe")
        
        if st.button("Créer"):
            sql= "insert into utilisateur(nom,prenom,bureau,bdd,acces,identifiant,password) values(%s,%s,%s,%s,%s,%s,%s)"
            val= (nom,prenom,bur,bdd,acc,identifiant,password)
>>>>>>> master
            mycursor.execute(sql,val)
            mydb.commit()
            st.success("Enregistrement réussi!!!")
            


    elif option=="Lire":
        st.subheader("Les utilisateurs dans la base")
        mycursor.execute("select * from utilisateur")
        result = mycursor.fetchall()
<<<<<<< HEAD
        result = pd.DataFrame(result, columns=['ID','Nom','Prénom','Bureau','Identifiant','Mot_de_passe','Base_de_donnees', 'Habilitation'])
        st.dataframe(result)

=======
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
>>>>>>> master


    elif option=="Modifier":
        st.subheader("Modifiier un enregistrement")
        id=st.number_input("Enter ID",min_value=1)

        mycursor.execute("select * from utilisateur")
<<<<<<< HEAD
        result = pd.DataFrame(mycursor.fetchall(), columns=['ID','Nom','Prénom','Bureau','Identifiant','Mot_de_passe','Base_de_donnees', 'Habilitation'])
        result = result[result.ID==id]

        if result.shape[0]==1:
            nom=st.text_input("nouveau Nom", result['Nom'].iloc[0])
            prenom=st.text_input("nouveau Prenom", result['Prénom'].iloc[0])
            bur=st.text_input("nouveau Bureau", result['Bureau'].iloc[0])
            identifiant=st.text_input("nouvel Identifiant de connexion", result['Identifiant'].iloc[0])
            password=st.text_input("nouveau Mot de passe", result['Mot_de_passe'].iloc[0])
            bdd=st.text_input("Base de données", result['Base_de_donnees'].iloc[0])
            acc=st.text_input("Privilège d'accès", result['Habilitation'].iloc[0])
            if st.button("Modifier"):
                sql="update utilisateur set nom=%s, prenom=%s, bureau=%s, identifiant=%s, password=%s, bdd=%s, acces=%s where id =%s"
                val= (nom,prenom,bur,identifiant,password,bdd,acc,id)
=======
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
>>>>>>> master
                mycursor.execute(sql,val)
                mydb.commit()
                st.success("Mise à jour réussie!!!")
        else:
            st.write("Cet identifiant n'est pas créé.")

<<<<<<< HEAD


    elif option=="Supprimer":
        st.subheader("Supprimer un enregistrement")
        id=st.number_input("Entrer l'ID",min_value=1)
        if st.button("Supprimer"):
            sql="delete from utilisateur where id =%s"
            val=(id,)
            mycursor.execute(sql,val)
            mydb.commit()
            st.success("Suppression réussie!!!")


=======
>>>>>>> master
if mycursor:
    if __name__ == "__main__":
        main()
else:
    st.write("Connexion impossible à établir")
<<<<<<< HEAD



=======
>>>>>>> master
