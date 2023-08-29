-- upgrade --
ALTER TABLE "ball" ADD COLUMN "tags" VARCHAR(400) NOT NULL;
ALTER TABLE "ball" ADD COLUMN "location" VARCHAR(60) NOT NULL;
-- downgrade --
ALTER TABLE "ball" DROP COLUMN "tags";
ALTER TABLE "ball" DROP COLUMN "location";
