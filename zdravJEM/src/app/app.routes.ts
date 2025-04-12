import { Routes } from '@angular/router';
import {LoginComponent} from './login/login.component';
import {HomeComponent} from './home/home.component';
import  {ScrollFeedComponent} from './scroll-feed/scroll-feed.component';

export const routes: Routes = [{ path: '', component: LoginComponent }, // show LoginComponent at '/'
  { path: 'home', component: HomeComponent },
  { path: 'scrollfeed', component: ScrollFeedComponent },



];
