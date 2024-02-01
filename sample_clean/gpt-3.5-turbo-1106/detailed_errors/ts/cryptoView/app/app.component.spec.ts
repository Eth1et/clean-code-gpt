import { TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { AppComponent } from './app.component';

describe('AppComponent', () => {
  let fixture: ComponentFixture<AppComponent>;
  let app: AppComponent;

  beforeEach(async () => {
    await configureTestingModule();
    fixture = createComponent();
    app = fixture.componentInstance;
  });

  it('should create the app', () => {
    expect(app).toBeTruthy();
  });

  it(`should have as title 'crypto-view'`, () => {
    expect(app.title).toEqual('crypto-view');
  });

  it('should render title', () => {
    const compiled = getCompiledTemplate(fixture);
    expect(compiled.textContent).toContain('crypto-view app is running!');
  });

  function configureTestingModule() {
    TestBed.configureTestingModule({
      imports: [RouterTestingModule],
      declarations: [AppComponent]
    }).compileComponents();
  }

  function createComponent() {
    return TestBed.createComponent(AppComponent);
  }

  function getCompiledTemplate(compiledFixture: ComponentFixture<AppComponent>) {
    return compiledFixture.nativeElement as HTMLElement;
  }
});