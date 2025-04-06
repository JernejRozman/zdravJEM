import { Component } from '@angular/core';
import { AuthService } from '../auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html'
})
export class LoginComponent {
  email = '';
  password = '';
  errorMsg = '';

  constructor(private authService: AuthService, private router: Router) {}

  login() {
    this.authService.login(this.email, this.password)
      .then(() => {
        // Redirect to a 'home' or 'dashboard' route upon success
        this.router.navigate(['/home']);
      })
      .catch(err => {
        this.errorMsg = err.message;
      });
  }

  register() {
    this.authService.register(this.email, this.password)
      .then(() => {
        // Optionally auto-login or direct user
        this.router.navigate(['/home']);
      })
      .catch(err => {
        this.errorMsg = err.message;
      });
  }
}
