// #include "pyinterp/poisson_grid_fill.hpp"
// #include "pyinterp/detail/math.hpp"
// #include <gtest/gtest.h>

// TEST(poisson, grid_fill) {
//   auto lon = Eigen::RowVectorXd::LinSpaced(11, -179, 179);
//   auto lat = Eigen::RowVectorXd::LinSpaced(5, -80, 80);

//   auto data = Eigen::Matrix<double, -1, -1>();

//   data.resize(lon.size(), lat.size());

//   for (auto ix = 0; ix < data.rows(); ++ix) {
//     for (auto iy = 0; iy < data.cols(); ++iy) {
//       data(ix, iy) =
//           ix % data.cols() == iy
//               ? std::numeric_limits<double>::quiet_NaN()
//               : std::sin(pyinterp::detail::math::radians(lon(ix))) *
//                     std::cos(pyinterp::detail::math::radians(lat(iy)));
//     }
//   }
//   data(0, 1) = data(10, 1) = std::numeric_limits<double>::quiet_NaN();

//   std::cout << data << std::endl;
//   std::cout << "***********" << std::endl;
//   auto mask = Eigen::Matrix<bool, -1, -1>(data.array().isNaN());
//   pyinterp::poisson::_set_zonal_average<double>(data, mask, 12);
//   std::cout << data << std::endl;
//   std::cout << "***********" << std::endl;
//   pyinterp::poisson::_grid_fill<double>(data, mask, true, 1e-4, 0.45, 12);
//   std::cout << data << std::endl;
//   std::cout << "***********" << std::endl;
// //     pyinterp::poisson::grid_fill<double>(data,
// pyinterp::poisson::kZonalAverage, true, 10, 1e-9, 0.45, 1);
// //   std::cout << data << std::endl;
// }
