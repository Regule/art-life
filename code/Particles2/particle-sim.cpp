#include <iostream>
#include <cmath>

//--------------------------------------------------------------------------------------------------
//                                             CLASS DECLARATIONS 
//--------------------------------------------------------------------------------------------------
class Vec2D;
class Kinematics;
class Dynamics;
class Particle;

//--------------------------------------------------------------------------------------------------
//                                          TWO DIMENSIONAL VECTOR 
//--------------------------------------------------------------------------------------------------

class Vec2D {
public:
    double x;
    double y;

    Vec2D() : x(0.0), y(0.0) {}
    Vec2D(double xVal, double yVal) : x(xVal), y(yVal) {}

    // Addition operator
    Vec2D operator+(const Vec2D& other) const {
        return Vec2D(x + other.x, y + other.y);
    }

    // Subtraction operator
    Vec2D operator-(const Vec2D& other) const {
        return Vec2D(x - other.x, y - other.y);
    }

    // Multiplication by a scalar
    Vec2D operator*(double scalar) const {
        return Vec2D(x * scalar, y * scalar);
    }

    // Division by a scalar
    Vec2D operator/(double scalar) const {
        // You can add checks to avoid division by zero if needed.
        return Vec2D(x / scalar, y / scalar);
    }

    // Dot product
    double dot(const Vec2D& other) const {
        return x * other.x + y * other.y;
    }

    // Magnitude (length) of the vector
    double magnitude() const {
        return std::sqrt(x * x + y * y);
    }

    // Normalize the vector (convert to unit vector)
    Vec2D normalize() const {
        double mag = magnitude();
        if (mag != 0.0) {
            return *this / mag;
        }
        return *this;
    }

  // Add other vector to this one in place (save results to this vector)
  void operator+=(const Vec2D& other){
    x += other.x;
    y += other.y;
  }
};

//--------------------------------------------------------------------------------------------------
//                                            PHYSICAL OBJECT 
//--------------------------------------------------------------------------------------------------
class Kinematics{
  Vec2D position;
  Vec2D velocity;
  Vec2D acceleration;

  void update(const Dynamics &d, double dt){
    position += velocity*dt;
    velocity += acceleration*dt;
  }
};

class Dynamics{
  double mass;
  double friction_coefficent;
  
};

class Particle{
  Kinematics kinematics;

};


//--------------------------------------------------------------------------------------------------
//                                             MAIN FUNCTION 
//--------------------------------------------------------------------------------------------------
int main() {
    Vec2D v1(3.0, 4.0);
    Vec2D v2(1.0, 2.0);

    Vec2D sum = v1 + v2;
    Vec2D difference = v1 - v2;
    Vec2D scaled = v1 * 2.5;
    Vec2D normalized = v1.normalize();

    std::cout << "v1 + v2 = (" << sum.x << ", " << sum.y << ")" << std::endl;
    std::cout << "v1 - v2 = (" << difference.x << ", " << difference.y << ")" << std::endl;
    std::cout << "v1 * 2.5 = (" << scaled.x << ", " << scaled.y << ")" << std::endl;
    std::cout << "Normalized v1 = (" << normalized.x << ", " << normalized.y << ")" << std::endl;
    std::cout << "Dot product of v1 and v2 = " << v1.dot(v2) << std::endl;
    std::cout << "Magnitude of v1 = " << v1.magnitude() << std::endl;

    return 0;
}

