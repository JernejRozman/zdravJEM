import { Component } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';

// `
//     <h2>Welcome Home!</h2>
//     <p>Signed in as: {{ userEmail || 'Unknown User' }}</p>
//     <button (click)="logout()">Logout</button>
//   `,

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
  standalone: false
})
export class HomeComponent {
  userEmail: string | null = null;

  constructor(private authService: AuthService, private router: Router) {
    const currentUser = this.authService.currentUser;
    this.userEmail = currentUser ? currentUser.email : null;
  }

  logout() {
    this.authService.logout().then(() => {
      this.router.navigate(['/login']);
    });
  }
}
