-- upgrade --
ALTER TABLE "ball" ADD COLUMN "tags" VARCHAR(400) ;
ALTER TABLE "ball" ADD COLUMN "location" VARCHAR(60) ;
-- downgrade --
ALTER TABLE "ball" DROP COLUMN "tags";
ALTER TABLE "ball" DROP COLUMN "location";
