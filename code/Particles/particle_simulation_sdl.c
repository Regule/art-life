#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <SDL2/SDL.h>

#define WINDOW_WIDTH 800
#define WINDOW_HEIGHT 600
#define NUM_PARTICLES 1000
#define NUM_COLORS 16

typedef struct {
    float x;
    float y;
    float vx;
    float vy;
    int color;
} Particle;

int colorForceMatrix[NUM_COLORS][NUM_COLORS];

Particle particles[NUM_PARTICLES];

void initializeParticles() {
    srand(time(NULL));

    for (int i = 0; i < NUM_PARTICLES; i++) {
        particles[i].x = (float)(rand() % WINDOW_WIDTH);
        particles[i].y = (float)(rand() % WINDOW_HEIGHT);
        particles[i].vx = ((float)rand() / RAND_MAX) * 2 - 1;
        particles[i].vy = ((float)rand() / RAND_MAX) * 2 - 1;
        particles[i].color = rand() % NUM_COLORS;
    }
}

void updateParticles(double dt) {
    for (int i = 0; i < NUM_PARTICLES; i++) {
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
        for (int j = 0; j < NUM_PARTICLES; j++) {
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

                    particles[i].vx += forceX;
                    particles[i].vy += forceY;
               // }
            }
        }
    }
}

void drawParticles(SDL_Renderer* renderer) {
    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
    SDL_RenderClear(renderer);

    for (int i = 0; i < NUM_PARTICLES; i++) {
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

    for (int i = 0; i < NUM_COLORS; i++) {
        for (int j = 0; j < NUM_COLORS; j++) {
            if(i==j){
              colorForceMatrix[i][j] == 1;
            }else{
              colorForceMatrix[i][j] = -1 + ((double)rand() / RAND_MAX) * 2; 
            }
        }
    }

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
        
        double dt = (timestamp - last_timestamp)/10.0;
        last_timestamp = timestamp;
        // Update particles
        updateParticles(dt); 
        // Draw particles
        drawParticles(renderer);
    }

    return 0;
}

