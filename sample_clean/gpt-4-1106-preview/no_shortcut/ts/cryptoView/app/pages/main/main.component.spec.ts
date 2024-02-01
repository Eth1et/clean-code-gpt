import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MainComponent } from './main.component';

describe('MainComponent Tests', () => {
  let mainComponent: MainComponent;
  let mainFixture: ComponentFixture<MainComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MainComponent ]
    }).compileComponents();

    mainFixture = TestBed.createComponent(MainComponent);
    mainComponent = mainFixture.componentInstance;
    mainFixture.detectChanges();
  });

  it('should create the component', () => {
    expect(mainComponent).toBeTruthy();
  });
});