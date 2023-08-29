-- upgrade --
ALTER TABLE "ball" ALTER COLUMN "economy_id" SET NOT NULL;
CREATE TABLE IF NOT EXISTS "newsarticle" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(512) NOT NULL,
    "content" TEXT NOT NULL,
    "date" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "ball"."tags" IS 'Provides details about the microball';
COMMENT ON COLUMN "newsarticle"."title" IS 'The title of the news article';
COMMENT ON COLUMN "newsarticle"."content" IS 'The content of the news article';
COMMENT ON COLUMN "newsarticle"."date" IS 'When the article was written';
-- downgrade --
ALTER TABLE "ball" ALTER COLUMN "economy_id" DROP NOT NULL;
DROP TABLE IF EXISTS "newsarticle";
