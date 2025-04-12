// app-routing.module.ts

import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

// Example: import your actual components
import { LoginComponent } from './components/login/login.component';
import { HomeComponent } from './components/home/home.component';
import {ScrollFeedComponent} from './components/scroll-feed/scroll-feed.component';
import { FriendsComponent} from './components/friends/friends.component';
import {PhotoCaptureComponent} from './components/photo-capture/photo-capture.component';

// Define your routes:
const routes: Routes = [
  { path: '', component: LoginComponent }, // show LoginComponent at '/'
  { path: 'home', component: HomeComponent },
  { path: 'scrollfeed', component: ScrollFeedComponent},
  { path: 'friends', component: FriendsComponent},
  { path: 'photo', component: PhotoCaptureComponent},

  // or anything else you need
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
