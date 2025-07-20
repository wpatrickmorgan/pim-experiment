/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  trailingSlash: true,
  images: {
    unoptimized: true
  },
  distDir: 'build',
  assetPrefix: '/assets/imperium_pim/frontend/build',
  basePath: '',
  typescript: {
    ignoreBuildErrors: false,
  },
  eslint: {
    ignoreDuringBuilds: false,
  },
  env: {
    NEXT_PUBLIC_API_BASE: '/api/method/imperium_pim.api',
  }
}

module.exports = nextConfig
