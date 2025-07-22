# PIM Experiment Frontend

A Next.js frontend designed to work seamlessly with Frappe PIM backend.

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## 🏗️ Built With

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first CSS framework
- **React Query** - Server state management
- **Zustand** - Client state management
- **React Hook Form** - Form handling

## 🔗 Frappe Integration

This frontend is specifically configured to integrate with Frappe backends:

- Uses relative URLs for all API calls
- Handles CSRF tokens automatically
- Integrates with Frappe session management
- Follows Frappe response format conventions

## 📁 Project Structure

```
src/
├── app/          # Next.js App Router pages
├── components/   # Reusable UI components
├── hooks/        # Custom React hooks
├── types/        # TypeScript type definitions
└── utils/        # Utility functions
```

## 🛠️ Development

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript compiler

## 📋 Builder.io Ready

This project is configured with comprehensive `.builderrules` to guide Builder.io in creating components that are fully compatible with the Frappe backend integration.

