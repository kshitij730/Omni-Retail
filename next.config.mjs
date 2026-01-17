/** @type {import('next').NextConfig} */
const nextConfig = {
    // Dynamic API routing for local dev and production
    async rewrites() {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
        return [
            {
                source: "/api/:path*",
                destination: `${apiUrl}/api/:path*`,
            },
        ];
    },
    async headers() {
        return [
            {
                source: "/api/:path*",
                headers: [
                    { key: "Access-Control-Allow-Credentials", value: "true" },
                    { key: "Access-Control-Allow-Origin", value: "*" },
                    { key: "Access-Control-Allow-Methods", value: "GET,DELETE,PATCH,POST,PUT" },
                    { key: "Access-Control-Allow-Headers", value: "X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version" },
                ]
            }
        ]
    },
    // Explicitly allow other origins (like LAN IPs) for Server Actions/API
    experimental: {
        serverActions: {
            allowedOrigins: ['localhost:3000', '192.168.1.5:3000', '192.168.*.*:*']
        }
    }
};

export default nextConfig;
