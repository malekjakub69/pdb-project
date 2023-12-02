const chai = require('chai');
const chaiHttp = require('chai-http');
const expect = chai.expect;

chai.use(chaiHttp);

const apiUrl = "http://localhost:5123/api";

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

describe("API Tests", function () {
    /*
    // Get ALL endpoint tests
    it("should get all users", function (done) {
        chai.request(apiUrl)
            .get('/users')
            .end(function (err, res) {
                expect(res).to.have.status(200);
                expect(res.body.data).to.be.a('array');
                done();
            });
    });

    it("should get all articles", function (done) {
        chai.request(apiUrl)
            .get('/articles')
            .end(function (err, res) {
                expect(res).to.have.status(200);
                expect(res.body.data).to.be.a('array');
                done();
            });
    });

    it("should get all regions", function (done) {
        chai.request(apiUrl)
            .get('/regions')
            .end(function (err, res) {
                expect(res).to.have.status(200);
                expect(res.body.data).to.be.a('array');
                done();
            });
    });

    // Region tests
    it("should create a region and delete it, verify sync", async function () {
        const newRegion = {
            iso_code: "US",
            country_name: "United States"
        };

        // Create a new region
        const createRegionResponse = await chai.request(apiUrl)
            .post('/mysql/region')
            .send(newRegion);
        expect(createRegionResponse).to.have.status(201);
        const createdRegionId = createRegionResponse.body.region.id;

        // Wait for 2 seconds
        await sleep(2000);

        // Get all regions
        const getAllRegionsResponse = await chai.request(apiUrl)
            .get('/regions');
        expect(getAllRegionsResponse).to.have.status(200);
        expect(getAllRegionsResponse.body.data).to.be.a('array');

        // Check if the created region is present
        const createdRegionInResponse = getAllRegionsResponse.body.data.find(region => region.id === createdRegionId);
        expect(createdRegionInResponse).to.not.be.undefined;

        // Delete the created region
        const deleteRegionResponse = await chai.request(apiUrl)
            .delete(`/mysql/region/${createdRegionId}`);
        expect(deleteRegionResponse).to.have.status(200);

        // Wait for 2 seconds
        await sleep(2000);

        // Check if the created region is not present after deletion
        // Get all regions
        const getAll2RegionsResponse = await chai.request(apiUrl)
            .get('/regions');
        expect(getAll2RegionsResponse).to.have.status(200);
        expect(getAll2RegionsResponse.body.data).to.be.a('array');

        const deletedRegionInResponse = getAll2RegionsResponse.body.data.find(region => region.id === createdRegionId);
        expect(deletedRegionInResponse).to.be.undefined;
    }).timeout(8000);

    // User tests
    it("should create a user and delete it, verify sync", async function () {
        const newUser = {
            username: "testuser",
            email: "testuser@example.com",
            first_name: "Test",
            last_name: "User"
        };

        // Create a new user
        const createUserResponse = await chai.request(apiUrl)
            .post('/mysql/user')
            .send(newUser);
        expect(createUserResponse).to.have.status(201);
        const createdUserId = createUserResponse.body.user.id;

        // Wait for 2 seconds
        await sleep(2000);

        // Get all users
        const getAllUsersResponse = await chai.request(apiUrl)
            .get('/users');
        expect(getAllUsersResponse).to.have.status(200);
        expect(getAllUsersResponse.body.data).to.be.a('array');

        // Check if the created user is present
        const createdUserInResponse = getAllUsersResponse.body.data.find(user => user.id === createdUserId);
        expect(createdUserInResponse).to.not.be.undefined;

        // Delete the created user
        const deleteUserResponse = await chai.request(apiUrl)
            .delete(`/mysql/user/${createdUserId}`);
        expect(deleteUserResponse).to.have.status(200);

        // Wait for 2 seconds
        await sleep(2000);

        // Check if the created user is not present after deletion
        // Get all users
        const getAll2UsersResponse = await chai.request(apiUrl)
            .get('/users');
        expect(getAll2UsersResponse).to.have.status(200);
        expect(getAll2UsersResponse.body.data).to.be.a('array');

        const deletedUserInResponse = getAll2UsersResponse.body.data.find(user => user.id === createdUserId);
        expect(deletedUserInResponse).to.be.undefined;
    }).timeout(8000);

    it("should create, not duplicate, and delete a user", function (done) {
        const testUser = { username: "Test User", email: "test@example.com", first_name: "test", last_name: "test" };

        // Create a new user
        chai.request(apiUrl)
            .post('/mysql/user')
            .send(testUser)
            .end(function (err, res) {
                expect(res).to.have.status(201);
                expect(res.body).to.be.a('object');
                const createdUserId = res.body.user.id;

                // Try to create the same user
                chai.request(apiUrl)
                    .post('/mysql/user')
                    .send(testUser)
                    .end(function (err, res) {
                        expect(res).to.have.status(400);

                        // Delete the user
                        chai.request(apiUrl)
                            .delete(`/mysql/user/${createdUserId}`)
                            .end(function (err, res) {
                                expect(res).to.have.status(200);

                                done();
                            });
                    });
            });
    });

    it("should create a user, create an article with that user as author, and delete the article", function (done) {
        const testUser = { username: "Test User", email: "test@example.com", first_name: "test", last_name: "test" };

        // Create a new user
        chai.request(apiUrl)
            .post('/mysql/user')
            .send(testUser)
            .end(function (err, res) {
                expect(res).to.have.status(201);
                expect(res.body).to.be.a('object');
                const createdUserId = res.body.user.id;

                const testArticle = { title: "Test Article", content: "Test Content", perex: "perex", author_id: createdUserId };

                // Create a new article
                chai.request(apiUrl)
                    .post('/mysql/article')
                    .send(testArticle)
                    .end(function (err, res) {
                        expect(res).to.have.status(201);
                        expect(res.body).to.be.a('object');
                        const createdArticleId = res.body.article.id;

                        // Delete the article
                        chai.request(apiUrl)
                            .delete(`/mysql/article/${createdArticleId}`)
                            .end(function (err, res) {
                                expect(res).to.have.status(200);

                                // Delete the user
                                chai.request(apiUrl)
                                    .delete(`/mysql/user/${createdUserId}`)
                                    .end(function (err, res) {
                                        expect(res).to.have.status(200);

                                        done();
                                    });
                            });
                    });
            });
    });

    it("should create an article with comments", function (done) {
        const testUser = { username: "Test User", email: "test@example.com", first_name: "test", last_name: "test" };

        // Create a new user
        chai.request(apiUrl)
            .post('/mysql/user')
            .send(testUser)
            .end(function (err, res) {
                expect(res).to.have.status(201);
                expect(res.body).to.be.a('object');
                const createdUserId = res.body.user.id;

                const testArticle = { title: "Test Article", content: "Test Content", perex: "perex", author_id: createdUserId };

                // Create a new article
                chai.request(apiUrl)
                    .post('/mysql/article')
                    .send(testArticle)
                    .end(function (err, res) {
                        expect(res).to.have.status(201);
                        expect(res.body).to.be.a('object');
                        const createdArticleId = res.body.article.id;

                        const comments = [
                            { comment: "Comment 1", author_id: createdUserId, article_id: createdArticleId, country_name: "Czech Republic" },
                            { comment: "Comment 2", author_id: createdUserId, article_id: createdArticleId, country_name: "Czech Republic" },
                            { comment: "Comment 3", author_id: createdUserId, article_id: createdArticleId, country_name: "Czech Republic" },
                            { comment: "Comment 4", author_id: createdUserId, article_id: createdArticleId, country_name: "Czech Republic" },
                            { comment: "Comment 5", author_id: createdUserId, article_id: createdArticleId, country_name: "Czech Republic" },
                            { comment: "Comment 6", author_id: createdUserId, article_id: createdArticleId, country_name: "Czech Republic" },
                            { comment: "Comment 7", author_id: createdUserId, article_id: createdArticleId, country_name: "Czech Republic" },
                            { comment: "Comment 8", author_id: createdUserId, article_id: createdArticleId, country_name: "Czech Republic" },
                            { comment: "Comment 9", author_id: createdUserId, article_id: createdArticleId, country_name: "Czech Republic" },
                            { comment: "Comment 10", author_id: createdUserId, article_id: createdArticleId, country_name: "Czech Republic" },
                            { comment: "Comment 11", author_id: createdUserId, article_id: createdArticleId, country_name: "Czech Republic" },
                        ];

                        // Add comments to the article
                        let commentCount = 0;
                        comments.forEach(comment => {
                            chai.request(apiUrl)
                                .post(`/mysql/comment`)
                                .send(comment)
                                .end(async function (err, res) {
                                    if (commentCount < 10) {
                                        expect(res).to.have.status(201);
                                        expect(res.body).to.be.a('object');
                                    } else {
                                        expect(res).to.have.status(500);
                                        expect(res.body).to.be.a('object');
                                    }
                                    await sleep(50);

                                    commentCount++;

                                    if (commentCount === comments.length) {
                                        // Delete the article
                                        chai.request(apiUrl)
                                            .delete(`/mysql/article/${createdArticleId}`)
                                            .end(function (err, res) {
                                                expect(res).to.have.status(200);

                                                // Delete the user
                                                chai.request(apiUrl)
                                                    .delete(`/mysql/user/${createdUserId}`)
                                                    .end(function (err, res) {
                                                        expect(res).to.have.status(200);

                                                        done();
                                                    });
                                            });
                                    }
                                });
                        });
                    });
            });
    });
*/
    it("should create users, articles with tags, assign likes and reads, call /api/trends/<string:timeframe>, and test feeds", function (done) {
        const users = [
            { username: "User1", email: "user1@example.com", first_name: "User", last_name: "One" }, // Author of all articles
            { username: "User2", email: "user2@example.com", first_name: "User", last_name: "Two" }, // Likes article2 with tag2 and 3, his feed should be article 1 and 3
            { username: "User3", email: "user3@example.com", first_name: "User", last_name: "Three" } // Does not read or like anything, feed should be empty
        ];

        const articles = [
            { title: "Article1", content: "Content1", perex: "Perex1", tags: ["tag1", "tag2"] },
            { title: "Article2", content: "Content2", perex: "Perex2", tags: ["tag2", "tag3"] },
            { title: "Article3", content: "Content3", perex: "Perex3", tags: ["tag1", "tag3"] }
        ];

        let userIds, articleIds;

        // Create users
        const createUserPromises = users.map(user =>
            chai.request(apiUrl)
                .post('/mysql/user')
                .send(user)
        );

        Promise.all(createUserPromises)
            .then(userResponses => {
                expect(userResponses.every(response => response.status === 201)).to.be.true;
                userIds = userResponses.map(response => response.body.user.id);

                // Assign "User1" as the author of all articles
                articles.forEach(article => {
                    article.author_id = userIds[0];
                });

                // Create articles
                const createArticlePromises = articles.map(article =>
                    chai.request(apiUrl)
                        .post('/mysql/article')
                        .send(article)
                );

                return Promise.all(createArticlePromises);
            })
            .then(async articleResponses => {
                try {
                    expect(articleResponses.every(response => response.status === 201)).to.be.true;
                    articleIds = articleResponses.map(response => response.body.article.id);

                    // Assign likes and reads
                    const likeAndReadPromises = [];
                    // "User2" reads article2
                    likeAndReadPromises.push(
                        chai.request(apiUrl)
                            .post(`/mysql/read`)
                            .send({ article_id: articleIds[1], user_id: userIds[1] })
                    );
                    // "User2" likes article2
                    likeAndReadPromises.push(
                        chai.request(apiUrl)
                            .post(`/mysql/like`)
                            .send({ article_id: articleIds[1], user_id: userIds[1] })
                    );

                    const likeAndReadResponses = await Promise.all(likeAndReadPromises);
                    expect(likeAndReadResponses.every(response => response.status === 201)).to.be.true;

                    // Wait for sync. Allowed is 3 seconds
                    await sleep(3000);

                    const timeframe = "week";

                    // Call /api/trends/<string:timeframe>
                    const trendsResponse = await chai.request(apiUrl).get(`/trends/${timeframe}`);
                    expect(trendsResponse).to.have.status(200);
                    expect(trendsResponse.body.data).to.be.an('array');

                    // Test feeds
                    const user3FeedResponse = await chai.request(apiUrl).get(`/user_feed/${userIds[2]}`); // "User3"
                    expect(user3FeedResponse).to.have.status(200);
                    expect(user3FeedResponse.body.data).to.be.an('array').that.is.empty; // Feed should be empty for "User3"

                    const user2FeedResponse = await chai.request(apiUrl).get(`/user_feed/${userIds[1]}`); // "User2"
                    expect(user2FeedResponse).to.have.status(200);

                    // Feed should have 1 and 3
                    expect(user2FeedResponse.body.data.map(item => item.id.toString())).to.include.members([
                        articleIds[0].toString(),
                        articleIds[2].toString()
                    ]);
                    // Article2 should not be in the feed as it is read
                    expect(user2FeedResponse.body.data.map(item => item.id.toString())).to.not.include(articleIds[1].toString());

                    // Ensure Article 2 is on top
                    expect(trendsResponse.body.data[0].article.id.toString()).to.equal(articleIds[1].toString());

                    // Assert read count and like count for Article 2
                    expect(trendsResponse.body.data[0].article.read_count.toString()).to.equal("1");
                    expect(trendsResponse.body.data[0].article.like_count.toString()).to.equal("1");

                    // Assert that article 1 and 3 are not in trends
                    const article1InTrends = trendsResponse.body.data.find(summary => summary.article.id == articleIds[0].toString());
                    const article3InTrends = trendsResponse.body.data.find(summary => summary.article.id == articleIds[2].toString());
                    expect(article1InTrends).to.not.exist; // Ensure Article 1 is not in the trends
                    expect(article3InTrends).to.not.exist; // Ensure Article 3 is not in the trends

                    // Clean up articles first
                    const deleteArticlePromises = articleIds.map(articleId =>
                        chai.request(apiUrl).delete(`/mysql/article/${articleId}`)
                    );

                    // Wait for all article deletions to finish
                    await Promise.all(deleteArticlePromises);

                    // Now clean up users
                    const deleteUserPromises = userIds.map(userId =>
                        chai.request(apiUrl).delete(`/mysql/user/${userId}`)
                    );

                    // Wait for all user deletions to finish
                    const deleteResponses = await Promise.all(deleteUserPromises);

                    expect(deleteResponses.every(response => response.status === 200)).to.be.true;
                    done();

                } catch (error) {
                    done(error);
                }
            });
    }).timeout(10000);

})