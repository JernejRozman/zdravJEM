import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

// The root component of your app
import { AppComponent } from './app.component';

// 1) AngularFire / Firebase
import { provideFirebaseApp, initializeApp } from '@angular/fire/app';
import { provideAuth, getAuth } from '@angular/fire/auth';
import { environment } from '../environments/environment';
import { provideFirestore, getFirestore } from '@angular/fire/firestore';

// 2) FormsModule (for ngModel in your login form)
import { FormsModule } from '@angular/forms';

// 3) Our routing module
import { AppRoutingModule } from './app-routing.module';

// 4) Declare your components
import { LoginComponent } from './components/login/login.component';
import { HomeComponent } from './components/home/home.component';
import {ScrollFeedComponent} from './components/scroll-feed/scroll-feed.component';
import { FriendsComponent } from './components/friends/friends.component';
import { PhotoCaptureComponent } from './components/photo-capture/photo-capture.component';
import {AngularFireModule} from '@angular/fire/compat';
import {AngularFireAuthModule} from '@angular/fire/compat/auth';



@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,  // must be declared if used in routes
    HomeComponent, // same here
    ScrollFeedComponent,
    FriendsComponent,
    PhotoCaptureComponent,

  ],
  imports: [
    BrowserModule,
    FormsModule,
    AppRoutingModule,
    AngularFireModule.initializeApp(environment.firebaseConfig),
    AngularFireAuthModule


  ],
  providers: [
    // Provide Firebase + Auth directly in the providers array
    provideFirebaseApp(() => initializeApp(environment.firebaseConfig)),
    provideAuth(() => getAuth())
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
