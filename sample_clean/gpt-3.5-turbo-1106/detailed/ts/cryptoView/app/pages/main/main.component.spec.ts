import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MainComponent } from './main.component';

describe('MainComponent', () => {
  let mainComponent: MainComponent;
  let fixture: ComponentFixture<MainComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [MainComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(MainComponent);
    mainComponent = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(mainComponent).toBeTruthy();
  });
});