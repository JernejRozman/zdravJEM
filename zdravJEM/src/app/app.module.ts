import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from './app.component';

// 1) Import these from AngularFire
import { provideFirebaseApp, initializeApp } from '@angular/fire/app';
import { provideAuth, getAuth } from '@angular/fire/auth';

// 2) Import the environment config
import { environment } from '../environments/environment';

// 3) For login form, you need FormsModule or ReactiveFormsModule
import { FormsModule } from '@angular/forms';

// (Optional) If you have routing
import { AppRoutingModule } from './app-routing.module';

@NgModule({
  declarations: [
    AppComponent,
    // We'll add our LoginComponent soon
  ],
  imports: [
    BrowserModule,
    FormsModule,                       // enable ngModel
    AppRoutingModule,                  // if using routing
    provideFirebaseApp(() => initializeApp(environment.firebase)),
    provideAuth(() => getAuth()),
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
