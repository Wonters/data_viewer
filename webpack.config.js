const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const { CleanWebpackPlugin } = require("clean-webpack-plugin");

module.exports = {
    mode: "development", // Change en "production" pour optimiser
    entry: "./src/js/main.js", // Fichier JS principal
    output: {
        filename: "main.bundle.js",
        path: path.resolve(__dirname, "src/static/dist"),
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: "babel-loader",
                    options: {
                        presets: ["@babel/preset-env"]
                    }
                }
            },
            {
                test: /\.css$/, // Gérer les fichiers CSS
                use: [MiniCssExtractPlugin.loader, "css-loader"]
            },
            {
                test: /\.(scss|sass)$/, // Gérer les fichiers SCSS
                use: [MiniCssExtractPlugin.loader, "css-loader", "sass-loader"]
            }
        ]
    },
    plugins: [
        new CleanWebpackPlugin(),
        new MiniCssExtractPlugin({ filename: "main.css" }),
    ],
    devServer: {
        static: path.join(__dirname, "static/dist"),
        compress: true,
        port: 9000
    }
};
