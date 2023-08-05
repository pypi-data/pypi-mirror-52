// This file is part of Eigen, a lightweight C++ template library
// for linear algebra.
//
// Copyright (C) 2010 Gael Guennebaud <gael.guennebaud@inria.fr>
//
// This Source Code Form is subject to the terms of the Mozilla
// Public License v. 2.0. If a copy of the MPL was not distributed
// with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

// The computeRoots function included in this is based on materials
// covered by the following copyright and license:
// 
// Geometric Tools, LLC
// Copyright (c) 1998-2010
// Distributed under the Boost Software License, Version 1.0.
// 
// Permission is hereby granted, free of charge, to any person or organization
// obtaining a copy of the software and accompanying documentation covered by
// this license (the "Software") to use, reproduce, display, distribute,
// execute, and transmit the Software, and to prepare derivative works of the
// Software, and to permit third-parties to whom the Software is furnished to
// do so, all subject to the following:
// 
// The copyright notices in the Software and this entire statement, including
// the above license grant, this restriction and the following disclaimer,
// must be included in all copies of the Software, in whole or in part, and
// all derivative works of the Software, unless such copies or derivative
// works are solely in the form of machine-executable object code generated by
// a source language processor.
// 
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT
// SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE
// FOR ANY DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE,
// ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
// DEALINGS IN THE SOFTWARE.

#include <iostream>
#include <Eigen/Core>
#include <Eigen/Eigenvalues>
#include <Eigen/Geometry>
#include <bench/BenchTimer.h>

using namespace Eigen;
using namespace std;

template<typename Matrix, typename Roots>
inline void computeRoots(const Matrix& m, Roots& roots)
{
  typedef typename Matrix::Scalar Scalar;
  const Scalar s_inv3 = 1.0/3.0;
  const Scalar s_sqrt3 = std::sqrt(Scalar(3.0));

  // The characteristic equation is x^3 - c2*x^2 + c1*x - c0 = 0.  The
  // eigenvalues are the roots to this equation, all guaranteed to be
  // real-valued, because the matrix is symmetric.
  Scalar c0 = m(0,0)*m(1,1)*m(2,2) + Scalar(2)*m(0,1)*m(0,2)*m(1,2) - m(0,0)*m(1,2)*m(1,2) - m(1,1)*m(0,2)*m(0,2) - m(2,2)*m(0,1)*m(0,1);
  Scalar c1 = m(0,0)*m(1,1) - m(0,1)*m(0,1) + m(0,0)*m(2,2) - m(0,2)*m(0,2) + m(1,1)*m(2,2) - m(1,2)*m(1,2);
  Scalar c2 = m(0,0) + m(1,1) + m(2,2);

  // Construct the parameters used in classifying the roots of the equation
  // and in solving the equation for the roots in closed form.
  Scalar c2_over_3 = c2*s_inv3;
  Scalar a_over_3 = (c1 - c2*c2_over_3)*s_inv3;
  if (a_over_3 > Scalar(0))
    a_over_3 = Scalar(0);

  Scalar half_b = Scalar(0.5)*(c0 + c2_over_3*(Scalar(2)*c2_over_3*c2_over_3 - c1));

  Scalar q = half_b*half_b + a_over_3*a_over_3*a_over_3;
  if (q > Scalar(0))
    q = Scalar(0);

  // Compute the eigenvalues by solving for the roots of the polynomial.
  Scalar rho = std::sqrt(-a_over_3);
  Scalar theta = std::atan2(std::sqrt(-q),half_b)*s_inv3;
  Scalar cos_theta = std::cos(theta);
  Scalar sin_theta = std::sin(theta);
  roots(2) = c2_over_3 + Scalar(2)*rho*cos_theta;
  roots(0) = c2_over_3 - rho*(cos_theta + s_sqrt3*sin_theta);
  roots(1) = c2_over_3 - rho*(cos_theta - s_sqrt3*sin_theta);
}

template<typename Matrix, typename Vector>
void eigen33(const Matrix& mat, Matrix& evecs, Vector& evals)
{
  typedef typename Matrix::Scalar Scalar;
  // Scale the matrix so its entries are in [-1,1].  The scaling is applied
  // only when at least one matrix entry has magnitude larger than 1.

  Scalar shift = mat.trace()/3;
  Matrix scaledMat = mat;
  scaledMat.diagonal().array() -= shift;
  Scalar scale = scaledMat.cwiseAbs()/*.template triangularView<Lower>()*/.maxCoeff();
  scale = std::max(scale,Scalar(1));
  scaledMat/=scale;

  // Compute the eigenvalues
//   scaledMat.setZero();
  computeRoots(scaledMat,evals);

  // compute the eigen vectors
  // **here we assume 3 differents eigenvalues**

  // "optimized version" which appears to be slower with gcc!
//     Vector base;
//     Scalar alpha, beta;
//     base <<   scaledMat(1,0) * scaledMat(2,1),
//               scaledMat(1,0) * scaledMat(2,0),
//              -scaledMat(1,0) * scaledMat(1,0);
//     for(int k=0; k<2; ++k)
//     {
//       alpha = scaledMat(0,0) - evals(k);
//       beta  = scaledMat(1,1) - evals(k);
//       evecs.col(k) = (base + Vector(-beta*scaledMat(2,0), -alpha*scaledMat(2,1), alpha*beta)).normalized();
//     }
//     evecs.col(2) = evecs.col(0).cross(evecs.col(1)).normalized();

//   // naive version
//   Matrix tmp;
//   tmp = scaledMat;
//   tmp.diagonal().array() -= evals(0);
//   evecs.col(0) = tmp.row(0).cross(tmp.row(1)).normalized();
// 
//   tmp = scaledMat;
//   tmp.diagonal().array() -= evals(1);
//   evecs.col(1) = tmp.row(0).cross(tmp.row(1)).normalized();
// 
//   tmp = scaledMat;
//   tmp.diagonal().array() -= evals(2);
//   evecs.col(2) = tmp.row(0).cross(tmp.row(1)).normalized();
  
  // a more stable version:
  if((evals(2)-evals(0))<=Eigen::NumTraits<Scalar>::epsilon())
  {
    evecs.setIdentity();
  }
  else
  {
    Matrix tmp;
    tmp = scaledMat;
    tmp.diagonal ().array () -= evals (2);
    evecs.col (2) = tmp.row (0).cross (tmp.row (1)).normalized ();
    
    tmp = scaledMat;
    tmp.diagonal ().array () -= evals (1);
    evecs.col(1) = tmp.row (0).cross(tmp.row (1));
    Scalar n1 = evecs.col(1).norm();
    if(n1<=Eigen::NumTraits<Scalar>::epsilon())
      evecs.col(1) = evecs.col(2).unitOrthogonal();
    else
      evecs.col(1) /= n1;
    
    // make sure that evecs[1] is orthogonal to evecs[2]
    evecs.col(1) = evecs.col(2).cross(evecs.col(1).cross(evecs.col(2))).normalized();
    evecs.col(0) = evecs.col(2).cross(evecs.col(1));
  }
  
  // Rescale back to the original size.
  evals *= scale;
  evals.array()+=shift;
}

int main()
{
  BenchTimer t;
  int tries = 10;
  int rep = 400000;
  typedef Matrix3d Mat;
  typedef Vector3d Vec;
  Mat A = Mat::Random(3,3);
  A = A.adjoint() * A;
//   Mat Q = A.householderQr().householderQ();
//   A = Q * Vec(2.2424567,2.2424566,7.454353).asDiagonal() * Q.transpose();

  SelfAdjointEigenSolver<Mat> eig(A);
  BENCH(t, tries, rep, eig.compute(A));
  std::cout << "Eigen iterative:  " << t.best() << "s\n";
  
  BENCH(t, tries, rep, eig.computeDirect(A));
  std::cout << "Eigen direct   :  " << t.best() << "s\n";

  Mat evecs;
  Vec evals;
  BENCH(t, tries, rep, eigen33(A,evecs,evals));
  std::cout << "Direct: " << t.best() << "s\n\n";

//   std::cerr << "Eigenvalue/eigenvector diffs:\n";
//   std::cerr << (evals - eig.eigenvalues()).transpose() << "\n";
//   for(int k=0;k<3;++k)
//     if(evecs.col(k).dot(eig.eigenvectors().col(k))<0)
//       evecs.col(k) = -evecs.col(k);
//   std::cerr << evecs - eig.eigenvectors() << "\n\n";
}
