/** @type {import('next').NextConfig} */
const nextConfig = {
  // Standard Next.js configuration for Vercel deployment
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
  
  // Environment variables for separate deployment
  env: {
    DEPLOYMENT_MODE: process.env.DEPLOYMENT_MODE || 'monorepo',
  },

  // CORS headers for API communication with Frappe backend
  async headers() {
    return [
      {
        source: '/api/:path*',
        headers: [
          { key: 'Access-Control-Allow-Credentials', value: 'true' },
          { key: 'Access-Control-Allow-Origin', value: process.env.NEXT_PUBLIC_API_BASE_URL || '*' },
          { key: 'Access-Control-Allow-Methods', value: 'GET,OPTIONS,PATCH,DELETE,POST,PUT' },
          { key: 'Access-Control-Allow-Headers', value: 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version' },
        ],
      },
    ]
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
