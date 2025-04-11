// app-routing.module.ts

import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

// Example: import your actual components
import { LoginComponent } from './components/login/login.component';
import { HomeComponent } from './components/home/home.component';

// Define your routes:
const routes: Routes = [
  { path: '', component: LoginComponent }, // show LoginComponent at '/'
  { path: 'home', component: HomeComponent }
  // or anything else you need
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
