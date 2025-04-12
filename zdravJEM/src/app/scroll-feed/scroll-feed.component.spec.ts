import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ScrollFeedComponent } from './scroll-feed.component';

describe('ScrollFeedComponent', () => {
  let component: ScrollFeedComponent;
  let fixture: ComponentFixture<ScrollFeedComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ScrollFeedComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ScrollFeedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
