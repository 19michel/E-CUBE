library(shiny)
data<-read.csv2("densites/NAFconso.csv")
data<-read.csv2("NAF.csv")
data<-read.csv2("sirene_conso.csv")
data<-read.csv2("departementsfrancais.csv")
secteur<-NAF$Intitulés.de.la.NAF
shinyUI(fluidPage(
  titlePanel(title= h3("Consomation électrique des entreprises",align="center")),
  
  sidebarLayout(
      sidebarPanel(h3("Données"),
        textInput("consoinput","Entrer le code SIRET de l'entreprise:",value=""),
        textInput("IRISinput","Entrer un IRIS:",value=""),
        selectizeInput("region","Par région",choices = departementsfrancais[1:13,8],options=list(placeholder = "choisir une région",
                                                                                            onInitialize = I('function() { this.setValue(""); }'))),
     selectizeInput("secteurinput","Par secteur d'activité", choices= secteur, options=list(placeholder = "choisir un secteur d'activité",
                                                                                            onInitialize = I('function() { this.setValue(""); }'))),
     radioButtons("globinput","Consommation moyenne par",choices = c("région","secteur d'activité"),selected = NULL),
    #sliderInput("Nbresectinput","",min=1,max=85,value = c(1,10))
    ),
        
      mainPanel(
        tabsetPanel(type="tab", 
                    tabPanel(h4("SIRET"),htmlOutput("données")),
                    tabPanel(h4("IRIS"),htmlOutput("IRIS2"), tableOutput("IRIS")),
                    tabPanel(h4("Région"),tableOutput("regionoutput"),plotOutput("plotregion"),tableOutput("tableregion")),
                    tabPanel(h4("Secteur"),tableOutput("apeoutput"),plotOutput("plotsecteur"),tableOutput("tablesecteur")))
                              

      
          ))))

