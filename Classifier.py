# This contains functions and classes

class classifier:
    
    # fit methods trains the data
    def fit(self,X,y,spar=10e-3): # here self is the variable which refers to current object of class 
        number_of_sample,number_of_features = X.shape # returns shape of X which is NxD dimensional
        # categories contains classes in Y uniquely due to Set
        self.categories=np.unique(y)
        
        # number_of_classes is the local variable
        number_of_classes=len(self.categories)
        
        # Initialising mean, var and priors
        self.classifier_mean=np.zeros((number_of_classes,number_of_features),dtype=np.float64)
        self.classifier_var=np.zeros((number_of_classes,number_of_features),dtype=np.float64)
        self.log_prior=np.zeros((number_of_classes),dtype=np.float64)
        
        # Calculating mean,var,prior based on categories in Y
        for classes in self.categories:
            X_classes=X[classes==y] # grouping into X_classes array according to category in y
            self.classifier_mean[classes,:]=X_classes.mean(axis=0) # mean with each row of sample belonging particular column(features)
            self.classifier_var[classes,:]=X_classes.var(axis=0)+spar
            self.log_prior[classes]=np.log(X_classes.shape[0]/float(number_of_sample)) #number of sample in a class/ total samples
            # i have logged prior because in posterior we will be calculation log_pdf in predict
            
        
        
        
    
    
    # predict method make prediction
    def predict(self,X):
        # posterior probablity dimension (number of sample,number of categories)
        posteriorS=np.zeros((X.shape[0],len(self.categories)))
        for classes in self.categories: # calculating posterior with log of class_conditional probablity + log prior 
            posteriorS[:,classes]=mvn.logpdf(X,
                                             mean=self.classifier_mean[classes,:],
                                             cov=self.classifier_var[classes,:]) + self.log_prior[classes]
        return np.argmax(posteriorS,axis=1)
        
    def accuracy(self,y_true,predicted):
        return np.mean(y_true==predicted)
        