import { Component } from '@angular/core';

@Component({
  selector: 'app-scroll-feed',
  standalone: false,
  templateUrl: './scroll-feed.component.html',
  styleUrl: './scroll-feed.component.css',
})
export class ScrollFeedComponent {

  handleReaction(event: Event): void {
    //console.log("Kliknjeno pizdica")
    const target = event.target as HTMLElement;
    // Add a class that scales the emoji up 20%
    target.classList.add('active');
    // Remove the class after 300ms so it returns to normal
    setTimeout(() => {
      target.classList.remove('active');
    }, 300);
  }
}
