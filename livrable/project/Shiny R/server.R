library(shiny)
shinyServer(
  function(input, output){
    data<-read.csv2("densites/NAFconso.csv")
    data<-read.csv2("NAF.csv")
    data<-read.csv2("sirene_conso.csv")
    data<-read.csv2("departementsfrancais.csv")
    NAFsecteur <- NAF[order(-NAF$Conso_moyenne.salarié), ]
    
    #output$soustitre<-renderText({if(input$globinput=="secteur d'activité"){paste(h4("Par secteur"))}
                      #else if(input$globinput=="région"){paste(h4("Par région"))}})
    
    output$plotsecteur <- renderPlot({
        if (input$globinput=="secteur d'activité"){
        barplot(NAFsecteur[1:10,3],names.arg=NAFsecteur[1:10,1],ylab= "Secteur d'activité", xlab= "Consommation par salarié (MWh)",xlim= c(0,20),horiz=TRUE,las=1,width=60)}
        })
    
    output$tablesecteur<-renderTable(
        if (input$globinput=="secteur d'activité"){
        NAFsecteur[1:10,]})
    
    output$plotregion <- renderPlot({
      if (input$globinput=="région"){
       mean<-rep(0,12)
       name<-rep(0,12)
       num<-seq(1,12)
       for (j in 1:12){l=which(sirene_conso$Region==departementsfrancais$V8[j])
       mean[j]<-summary(as.numeric(sirene_conso[l,12]))[4]
       name[j]<-departementsfrancais$V8[j]}
       barplot(mean,names.arg=num[1:12],ylab= "Région", xlab= "Consommation moyenne (MWh)",xlim= c(0,200),horiz=TRUE,las=1,width=60)}
    })
    
    output$tableregion<-renderTable({
      if (input$globinput=="région"){
        Consommation.moyenne<-rep(0,12)
        région<-rep(0,12)
        num.région<-seq(1,12)
        for (j in 1:12){l=which(sirene_conso$Region==departementsfrancais$V8[j])
        Consommation.moyenne[j]<-summary(as.numeric(sirene_conso[l,12]))[4]
        région[j]<-departementsfrancais$V8[j]}
        
        regiondf<-data.frame(num.région,région,Consommation.moyenne)
        regiondf}})
  
    
    output$données<-renderText({
        i<-0
        if(input$consoinput!=""){
        i=which(sirene_conso[,4]==input$consoinput) }
        if(i!=0){
            str0<-paste("Numéro IRIS:",sirene_conso[i,2])
            str1<-paste("Numéro SIRET:",sirene_conso[i,4])
            str2<-paste("Nom de l'entreprise: ", sirene_conso[i,10])
            str3 <- paste("Nombre de salarié moyen:",floor(as.numeric(sirene_conso[i,6])))
            str4 <- paste("Consomation moyenne par an: ",sirene_conso[i,12],"MWh")
            str01<-paste(h4("Données Entreprise:"))
            HTML(paste(str01,str0,str1,str2,str3,str4, sep = '<br/>'))
          }}) 
    
    output$IRIS2<-renderText( 
            if(input$IRISinput!=""){paste(h4("Données par IRIS"))})
    
    output$IRIS <- renderTable({
            if(input$IRISinput!=""){j=which(sirene_conso$IRIS==input$IRISinput)
            sirene_conso[j,c(-1,-2,-3,-5,-7,-8)]}})
    
   output$regionoutput<-renderTable({if(input$region!=""){k=which(sirene_conso$Region==input$region)
           a<-sirene_conso[k,c(-1,-2,-3,-5,-7,-8,-13)]
           b<-a[order(as.numeric(as.character(a$ConsommationEntreprise)),decreasing = TRUE),]
           head(b,10)}})
   
   output$apeoutput<-renderTable({if(input$secteurinput!=""){
     l<-NAF[which(NAF$Intitulés.de.la.NAF==input$secteurinput),1]
     m<-which(sirene_conso$APE==l)
   a<-sirene_conso[m,c(-1,-2,-3,-5,-7,-8,-13)]
   b<-a[order(as.numeric(as.character(a$ConsommationEntreprise)),decreasing = TRUE),]
   head(b,10)}})
          
      

  })


  



