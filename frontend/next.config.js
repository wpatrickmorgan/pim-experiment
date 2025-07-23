/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable static export for deployment
  output: 'export',
  trailingSlash: true,
  skipTrailingSlashRedirect: true,
  // Disable image optimization for static export
  images: {
    unoptimized: true
  },
  typescript: {
    // !! WARN !!
    // Dangerously allow production builds to successfully complete even if
    // your project has type errors.
    // !! WARN !!
    ignoreBuildErrors: false,
  },
  eslint: {
    // Warning: This allows production builds to successfully complete even if
    // your project has ESLint errors.
    ignoreDuringBuilds: false,
  },
  // Configure asset prefix for proper loading
  assetPrefix: process.env.NODE_ENV === 'production' ? '' : '',
  
  // Environment variables for separate deployment
  env: {
    DEPLOYMENT_MODE: process.env.DEPLOYMENT_MODE || 'monorepo',
  },

  // Enhanced webpack configuration for cross-origin deployment
  webpack: (config, { buildId, dev, isServer, defaultLoaders, webpack }) => {
    // Add environment info to build
    config.plugins.push(
      new webpack.DefinePlugin({
        'process.env.BUILD_TIME': JSON.stringify(new Date().toISOString()),
        'process.env.BUILD_ID': JSON.stringify(buildId),
      })
    );
    
    return config
  },
}

module.exports = nextConfig
