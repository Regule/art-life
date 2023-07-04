#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <SDL2/SDL.h>

//--------------------------------------------------------------------------------------------------
//                                              CONFIGURATION
//--------------------------------------------------------------------------------------------------

#define WINDOW_WIDTH 800
#define WINDOW_HEIGHT 600
#define MAX_PARTICLE_COUNT 1000
#define MAX_NUMBER_OF_COLORS 16

int particle_count = MAX_PARTICLE_COUNT;
int number_of_colors = 4;

//--------------------------------------------------------------------------------------------------
//                                          PARTICLE MODEL 
//--------------------------------------------------------------------------------------------------
typedef struct {
    double x;
    double y;
    double vx;
    double vy;
    int color;
} Particle;

float colorForceMatrix[MAX_NUMBER_OF_COLORS][MAX_NUMBER_OF_COLORS];

void generate_random_force_matrix(){
  for (int i = 0; i < number_of_colors; i++) {
      for (int j = 0; j < number_of_colors; j++) {
        colorForceMatrix[i][j] = (-1 + ((double)rand() / RAND_MAX) * 2)*0.00001; 
        printf("Color %d attracts color %d with %f force\n",i,j,colorForceMatrix[i][j]);
      }
  }
}

Particle particles[MAX_PARTICLE_COUNT];

Particle initialize_random_particle(){
  Particle p;
  p.x = (float)(rand() % WINDOW_WIDTH);
  p.y = (float)(rand() % WINDOW_HEIGHT);
  p.vx = 0.0; //((float)rand() / RAND_MAX) * 2 - 1;
  p.vy = 0.0; //((float)rand() / RAND_MAX) * 2 - 1;
  p.color = rand() % number_of_colors;
  return p;
}

void initializeParticles() {
    srand(time(NULL));

    for (int i = 0; i < particle_count; i++) {
      particles[i] = initialize_random_particle();
    }
}

void updateParticles(double dt) {
    for (int i = 0; i < MAX_PARTICLE_COUNT; i++) {
        particles[i].x += particles[i].vx*dt;
        particles[i].y += particles[i].vy*dt;

        // Bounce off walls
        if (particles[i].x < 0 || particles[i].x > WINDOW_WIDTH) {
            particles[i].vx *= -1;
        }
        if (particles[i].y < 0 || particles[i].y > WINDOW_HEIGHT) {
            particles[i].vy *= -1;
        }

        // Apply interactions with other particles
        for (int j = 0; j < particle_count; j++) {
            if (i != j) {
                float dx = particles[j].x - particles[i].x;
                float dy = particles[j].y - particles[i].y;
                float distance = sqrt(dx * dx + dy * dy);

               // if (distance < 5) {
                    // Bounce on collision
               //     particles[i].vx *= -1;
               //     particles[i].vy *= -1;
               // } else {
                    // Determine force based on colors
                    int color1 = particles[i].color;
                    int color2 = particles[j].color;
                    float force = colorForceMatrix[color1][color2];

                    // Apply attraction or repulsion
                    float forceX = force * dx / distance;
                    float forceY = force * dy / distance;

                    particles[i].vx += forceX*dt;
                    particles[i].vy += forceY*dt;
               // }
            }
        }
    }
}

//--------------------------------------------------------------------------------------------------
//                                         VISUALISATION  
//--------------------------------------------------------------------------------------------------
void drawParticles(SDL_Renderer* renderer) {
    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
    SDL_RenderClear(renderer);

    for (int i = 0; i < particle_count; i++) {
        SDL_SetRenderDrawColor(renderer,
            (particles[i].color % 8) * 32,
            (particles[i].color % 4) * 64,
            (particles[i].color % 2) * 128,
            255
        );

        SDL_Rect rect = {
            (int)particles[i].x - 2,
            (int)particles[i].y - 2,
            4,
            4
        };

        SDL_RenderFillRect(renderer, &rect);
    }

    SDL_RenderPresent(renderer);
}

int main() {
    // Initialize SDL
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        printf("SDL could not initialize! SDL_Error: %s\n", SDL_GetError());
        return -1;
    }

    // Create window
    SDL_Window* window = SDL_CreateWindow("Particle Simulation",
        SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
        WINDOW_WIDTH, WINDOW_HEIGHT, SDL_WINDOW_SHOWN);
    if (window == NULL) {
        printf("Window could not be created! SDL_Error: %s\n", SDL_GetError());
        return -1;
    }

    // Create renderer
    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (renderer == NULL) {
        printf("Renderer could not be created! SDL_Error: %s\n", SDL_GetError());
        return -1;
    }

    generate_random_force_matrix();

    // Initialize particles
    initializeParticles();

    Uint32 last_timestamp = SDL_GetTicks();
    // Simulation loop
    while (1) {
        // Handle events
        SDL_Event event;
        while (SDL_PollEvent(&event)) {
            if (event.type == SDL_QUIT) {
                // Quit the program
                SDL_DestroyRenderer(renderer);
                SDL_DestroyWindow(window);
                SDL_Quit();
                return 0;
            }
        }

        Uint32 timestamp = SDL_GetTicks();
        
        double dt = (timestamp - last_timestamp)/1.0;
        last_timestamp = timestamp;
        // Update particles
        updateParticles(dt); 
        // Draw particles
        drawParticles(renderer);
    }

    return 0;
}

