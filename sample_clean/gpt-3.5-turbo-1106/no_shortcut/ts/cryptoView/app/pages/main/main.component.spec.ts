import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MainComponent } from './main.component';

describe('MainComponent', () => {
  let mainComponent: MainComponent;
  let componentFixture: ComponentFixture<MainComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [MainComponent]
    }).compileComponents();

    componentFixture = TestBed.createComponent(MainComponent);
    mainComponent = componentFixture.componentInstance;
    componentFixture.detectChanges();
  });

  it('should create', () => {
    expect(mainComponent).toBeTruthy();
  });
});