// next 와 jest 를 연동
const nextJest = require("next/jest");

//  여기에 있는 설정파일들을 읽어라(설정파일들은 이 공간에 다 있어)
const createJestConfig = nextJest({dir:'./'});

const jestConfig = {
    testEnvironment:'jest-environment-jsdom',
    moduleNameMapper: {
        '^@/(.*)$':'<rootDir>/src/$1'
    },
    setupFilesAfterEnv: ['<rootDir>/jest.setup.js'] // 테스트 전에 환경설정하는 용도
};

module.exports = createJestConfig(jestConfig);