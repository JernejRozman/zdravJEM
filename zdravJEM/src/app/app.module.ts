// app.module.ts

import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

// The root component of your app
import { AppComponent } from './app.component';

// 1) AngularFire / Firebase
import { provideFirebaseApp, initializeApp } from '@angular/fire/app';
import { provideAuth, getAuth } from '@angular/fire/auth';
import { environment } from '../environments/environment';

// 2) FormsModule (for ngModel in your login form)
import { FormsModule } from '@angular/forms';

// 3) Our routing module
import { AppRoutingModule } from './app-routing.module';

// 4) Declare your components
import { LoginComponent } from './login/login.component';
import { HomeComponent } from './home/home.component';
import {ScrollFeedComponent} from './scroll-feed/scroll-feed.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,  // must be declared if used in routes
    HomeComponent,    // same here
    ScrollFeedComponent,
  ],
  imports: [
    BrowserModule,
    FormsModule,
    AppRoutingModule,
    // Provide Firebase + Auth
    provideFirebaseApp(() => initializeApp(environment.firebase)),
    provideAuth(() => getAuth()),
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
